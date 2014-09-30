from patch_extractor.actions import delete_action


def _is_conflict(patch1, patch2):
    return (patch1.path == patch2.path
            and patch1.action != delete_action
            and patch2.action != delete_action)


def _auto_resolve(patch1, patch2):
    if patch1.value == patch2.value:
        return patch1


def merge_dict_patch(patch1, record1_patches, record2_patches, record1, record2, rules, conflicts):
    for patch2 in record2_patches:
        conflict = _is_conflict(patch1, patch2)
        if conflict:
            try:
                #TODO: a keep both might also be possible...
                #       * probably not though
                to_keep = _auto_resolve(patch1, patch2)
                if not to_keep:
                    to_keep = rules[tuple(patch1.path)](patch1, patch2,
                                                        record1, record2)

                # Reordering here shouldn't be a problem
                patch1.take = to_keep
                patch2.take = None
            except KeyError as e:
                conflicts.append(('no_rule', patch1, patch2, e.message))
            except Exception as e:
                conflicts.append(('merge_not_possible', patch1, patch2, e.message))


