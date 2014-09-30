# TODO: the conversion to a tuple might be a bad idea...
from itertools import izip_longest
from rule_manager import MergeRuleManager

from patch_extractor.actions import insert_action, delete_action


class MergeConflict(Exception):
    def __init__(self, message, data):
        self.message = message
        self.data = data


rule_manager = MergeRuleManager()
rule_manager.load_rules('rules')


def _filter_patches(patches, rules):
    filtered_patches = []
    for patch in patches:
        try:
            if rules[tuple(patch.path)](patch):
                filtered_patches.append(patch)
        except KeyError:
            filtered_patches.append(patch)

    return filtered_patches


def filter_patches_for_comparsion(patches, source1, source2):
    rules = rule_manager.get_rules(source1, source2)['COMPARSION']
    return _filter_patches(patches, rules)


def filter_patches(patches, source1, source2, patches_source):
    rules = rule_manager.get_rules(source1, source2)['FILTERING'][patches_source]
    return _filter_patches(patches, rules)


def _is_super_path(path1, path2):
    return all(map(lambda x: x[0] == x[1] or x[0] == None,
                   izip_longest(path1, path2)))


def _is_conflict(patch1, patch2):
    # TODO: This needs a lot of work now...
    # TODO: Create a list of defined conflicts
    #       * everything conflicts with delete if it has the same path or a more specific one
    if patch2.conflict_with == patch1:
        return True, patch1.path
    if patch1.path == patch2.old_patch:
        return True, patch1.path
    elif _is_super_path(patch1.path, patch2.path):
        return True, patch1.path
    elif _is_super_path(patch2.path, patch1.path):
        return True, patch2.path
    return False


def _auto_resolve(patch1, patch2):
    if (patch1.path == patch2.path
        and patch1.value == patch2.value):
        return patch1


# TODO: implement
# probably useless
def _is_list(_):
    return True


# TODO: Make this prettier
# probably useless
# two conflicting inserts with different len(value), how to shift the rest?
# -> rework the merge alogrithm in general
def _resolve_list_problems(record1_patches, record2_patches):
    for patch1 in record1_patches:
        if patch1.action == insert_action and _is_list(patch1):
            for patch2 in record2_patches:
                if _is_super_path(patch1.path[:-1], patch2.path):
                    if patch1.path[-1] < patch2.path[-1]:
                        patch2.path[-1] += len(patch1.value)
        elif patch1.action == delete_action and _is_list(patch1):
            for patch2 in record2_patches:
                if _is_super_path(patch1.path[:-1], patch2.path):
                    if patch1.path[-1] < patch2.path[-1]:
                        patch2.path[-1] -= patch1.value
                        if patch2.path[-1] < 0:
                            i = patch2.path[-1]
                            if patch2.action == delete_action:
                                patch2.path = 0
                                patch2.value += i       # i is negative
                            else:
                                patch2.conflict_with = patch1


# TODO: let's give this method the latest records, so the merging can be more powerful
def merge_patches(record1_patches, record2_patches, source1, source2,
                  record1, record2):
    rules = rule_manager.get_rules(source1, source2)['MERGING']

    #TODO: multiple conflicts are possible....
    self._resolve_list_problems(record1_patches, record2_patches)
    
    _merge_dict = {}
    _id = 0
    _conflicts = []
    for patch1 in record1_patches:
        for patch2 in record2_patches:
            conflict, path = _is_conflict(patch1, patch2)
            if conflict:
                try:
                    #TODO: a keep both might also be possible...
                    #       * probably not though
                    to_keep = _auto_resolve(patch1, patch2)
                    if not to_keep:
                        to_keep = rules[tuple(path)](patch1, patch2,
                                                     record1, record2)
                    _merge_dict[_id] = to_keep
                    try:
                        del _merge_dict[patch1.merged_with]
                    except KeyError:
                        pass
                    except AttributeError:
                        pass
                    patch1.merged_with = _id
                    patch2.merged_with = _id
                except KeyError as e:
                    _conflicts.append(('no_rule', patch1, patch2, e.message))
                    pass
                except Exception as e:
                    _conflicts.append(('merge_not_possible', patch1, patch2, e.message))
                    pass
            _id += 1

    if _conflicts:
        raise MergeConflict('merge conflict', _conflicts)

    filtered_patches = []
    for patch in record1_patches + record2_patches:
        if hasattr(patch, 'merged_with'):
            try:
                filtered_patches.append(_merge_dict[patch.merged_with])
                del _merge_dict[patch.merged_with]
            except KeyError:
                pass
        else:
            filtered_patches.append(patch)

    return filtered_patches
