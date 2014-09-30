# TODO: the conversion to a tuple might be a bad idea...
from rule_manager import MergeRuleManager

from dict_patch_merge import merge_dict_patch
from list_patch_merge import merge_list_patch


class MergeConflict(Exception):
    def __init__(self, message, data):
        self.message = message
        self.data = data


rule_manager = MergeRuleManager()
rule_manager.load_rules('rules')


def _filter_patches(record, patches, rules):
    filtered_patches = []
    for patch in patches:
        try:
            path = rules.query_path(tuple(patch.path))
            if rules[path](record, patch, patches, path[:-1]):
                filtered_patches.append(patch)
        except KeyError:
            filtered_patches.append(patch)

    return filtered_patches


def filter_patches_for_comparsion(record, patches, source1, source2):
    rules = rule_manager.get_rules(source1, source2)['COMPARSION']
    return _filter_patches(record, patches, rules)


def filter_patches(record, patches, source1, source2, patches_source):
    rules = rule_manager.get_rules(source1, source2)['FILTERING'][patches_source]
    return _filter_patches(record, patches, rules)


def _determine_environment(record, patch):
    env = record
    for p in patch.path[:-1]:
        env = env.__getitem__(p)

    if isinstance(env, list):
        return 'list'
    elif isinstance(env, dict):
        return 'dict'


# TODO: let's give this method the latest records, so the merging can be more powerful
def merge_patches(record1_patches, record2_patches, source1, source2,
                  record1, record2):
    rules = rule_manager.get_rules(source1, source2)['MERGING']

    # Step1: Group the patches to find possible conflicts quicker
    #        basically means to 'map' all patches form rec2 which are in a list
    #        to the corresponding patch in rec1
    #        we need two groups actually... one for each patch stack
    
    conflicts = []
    for patch1 in record1_patches:
        #Step2: Find the environment to decide if it is a list or not
        # TODO: This can be put into a list to make it even shorter
        environment = _determine_environment(record1, patch1)
        if environment == 'list':
            merge_list_patch(patch1, record1_patches, record2_patches, record1, record2, rules, conflicts)
        elif environment == 'dict':
            merge_dict_patch(patch1, record1_patches, record2_patches, record1, record2, rules, conflicts)

    if conflicts:
        raise MergeConflict('merge conflict', _conflicts)

    filtered_patches = []
    for patch in record1_patches + record2_patches:
        if hasattr(patch, 'take'):
            if patch.take:
                filtered_patches.append(patch.take)
        else:
            filtered_patches.append(patch)

    return filtered_patches
