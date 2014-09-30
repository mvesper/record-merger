from ConfigParser import ConfigParser
from utils import get_filenames_from_directory, WildcardDict
from copy import deepcopy
from itertools import izip_longest

from plugin_facade import MergeActionFinder
from patch_extractor.actions import replace_action
from patch_extractor.data import Patch


def _is_super_path(path1, path2):
    return all(map(lambda x: x[0] == x[1] or x[0] is None,
                   izip_longest(path1, path2)))


def ignore_patch(record, patch, patches, path):
    return False


def group_patches(record, patch, patches, path):
    if hasattr(patch, 'grouped'):
        return False

    record_val = record
    for _path in path[:-1]:
        record_val = record_val.__getitem__(_path)

    patch.path = list(path[:-1])
    patch.value = deepcopy(record_val)
    patch.action = replace_action

    for _patch in patches:
        if _is_super_path(path[:-1], _patch.path):
            _patch.grouped = True

    return True


def pick_source1(patch1, patch2, record1, record2):
    return patch1


def pick_source2(patch1, patch2, record1, record2):
    return patch2


def create_combine(action_string):
    _, source1_fields, source2_fields = [x.split(',') for x
                                         in action_string.split('-')]


    def closure(patch1, patch2, record1, record2):
        tmp = {}
    
        if '*' in source1_fields:
            fields_collection = [source1_fields, source2_fields]
            patches = [patch1, patch2]
        elif '*' in source2_fields:
            fields_collection = [source2_fields, source1_fields]
            patches = [patch2, patch1]
        else:
            fields_collection = [source1_fields, source2_fields]
            patches = [patch1, patch2]

        for source_fields, patch in zip(fields_collection, patches):
            if '*' in source_fields:
                tmp = deepcopy(patch.value)
            else:
                for field in source_fields:
                    tmp[field] = deepcopy(patch.value[field])

        patch = Patch()
        patch.path = deepcopy(patch1.path)
        patch.value = tmp
        patch.action = patch1.action

        return patch

    return closure


class MergeRuleManager:
    def __init__(self):
        self.rules = {}
        self.action_finder = MergeActionFinder()

    def load_rules(self, path):
        files = get_filenames_from_directory(path)
        for f in files:
            rule_set_name = self.extract_rule_set_name(f)
            config = ConfigParser()
            config.readfp(open(f))

            source1 = config.get('CONFIG', 'source1')
            source2 = config.get('CONFIG', 'source2')

            comparsion_dict = WildcardDict()
            for item in config.items('COMPARSION'):
                key = tuple(item[0].split(', '))
                comparsion_dict[key] = self.find_action(source1, source2, item[1])

            filtering_dict = {}
            source1_dict = WildcardDict()
            source2_dict = WildcardDict()
            for item in config.items('FILTERING'):
                key = tuple(item[0].split(', '))
                s1_action, s2_action = self.split_for_sources(item[1])

                s1_action = self.find_action(source1, source2, s1_action)
                s2_action = self.find_action(source1, source2, s2_action)

                if s1_action:
                    source1_dict[key] = s1_action

                if s2_action:
                    source2_dict[key] = s2_action

            filtering_dict[source1] = source1_dict
            filtering_dict[source2] = source2_dict

            merging_dict = WildcardDict()
            for item in config.items('MERGING'):
                key = tuple(item[0].split(', '))
                merging_dict[key] = self.find_action(source1, source2, item[1])

            tmp = {}
            tmp['COMPARSION'] = comparsion_dict
            tmp['FILTERING'] = filtering_dict
            tmp['MERGING'] = merging_dict

            self.rules[rule_set_name] = tmp

    def extract_rule_set_name(self, f):
        return f.split('/')[-1].replace('.conf', '')

    def split_for_sources(self, raw):
        return [x.strip() for x in raw.split(',')]

    def find_action(self, source1, source2, action_string):
        if action_string == '':
            return None
        elif action_string == 'ignore':
            return ignore_patch
        elif action_string == 'group':
            return group_patches 
        elif action_string == 'pick1':
            return pick_source1 
        elif action_string == 'pick2':
            return pick_source2 
        elif action_string.startswith('combine'):
            return create_combine(action_string)
        else:
            return self.action_finder.get_actions(source1, source2).get_action(action_string)

    def get_rules(self, source1, source2):
        return self.rules[source1 + '_' + source2]
