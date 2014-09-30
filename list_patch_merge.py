from patch_extractor.actions import insert_action, replace_action, delete_action


CFG_VALUE_BASED_LIST_MERGE = True


def _is_value_conflict(patch1, patch2):
    problem_actions = [replace_action, delete_action]
    if patch1.path == patch2.path:
        if patch1.action in problem_actions and patch2.action in problem_actions:
            return True
    return False


def _auto_resolve(patch1, patch2):
    if patch1.value == patch2.value:
        return patch1


def _shift(patches, list_path, _index, amount):
    i = 0
    for patch in patches:
        if patch.path[:-1] == list_path:
            if patch.path[-1] >= _index:
                patch.path[-1] += amount
                if patch.path[-1] < i:
                    patch.path[-1] = i
                    i += 1


def _shift_left(patches, list_path, _index, amount=1):
    _shift(patches, list_path, _index, -amount)


def _shift_right(patches, list_path, _index, amount=1):
    _shift(patches, list_path, _index, amount)


def merge_list_patch(patch1, record1_patches, record2_patches, record1, record2, rules, conflicts):
    if CFG_VALUE_BASED_LIST_MERGE:
        list_path = patch1.path[:-1]
        _index = patch1.path[-1]
        for patch2 in record2_patches:
            conflict = _is_value_conflict(patch1, patch2)
            if conflict:
                try:
                    #TODO: a keep both might also be possible...
                    #       * probably not though
                    to_keep = _auto_resolve(patch1, patch2)
                    if not to_keep:
                        to_keep = rules[tuple(path)](patch1, patch2,
                                                     record1, record2)

                    patch1.take = to_keep
                    patch2.take = None

                    # TODO: Does this work if we create a new patch?
                    if patch1.action == to_keep.action:
                        pass
                    elif patch1.action == delete_action and to_keep.action == replace_action:
                        _shift_right(record1_patches, list_path, _index)
                    elif patch1.action == replace_action and to_keep.action == delete_action:
                        _shift_left(record1_patches, list_path, _index)

                    if patch2.action == to_keep.action:
                        pass
                    elif patch2.action == delete_action and to_keep.action == replace_action:
                        _shift_right(record2_patches, list_path, _index)
                    elif patch2.action == replace_action and to_keep.action == delete_action:
                        _shift_left(record2_patches, list_path, _index)
                except KeyError as e:
                    # In case of a conflict, just give all the list patches...
                    conflicts.append(('no_rule', patch1, patch2, e.message))
                except Exception as e:
                    # In case of a conflict, just give all the list patches...
                    conflicts.append(('merge_not_possible', patch1, patch2, e.message))

                break
        else:
            if patch1.action == delete_action:
                _shift_left(record2_patches, list_path, _index)
            elif patch1.action == insert_action:
                _shift_right(record2_patches, list_path, _index)
    else:
        # This needs a lot of thought :/
        pass
