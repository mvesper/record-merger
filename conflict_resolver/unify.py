def _assign_conflict_index(conflicts):
    for i, (patches1, patches2) in enumerate(conflicts):
        for patch in patches1+patches2:
            try:
                patch['!@#$c_index'] = i
            except TypeError:
                pass
            

def _reassign_groups(patches):
    group_mapping = {}

    count = 0

    for patch in patches:
        if patch['group'] is not None:
            if '!@#$c_index' not in patch:
                patch['group'] = count
                continue
            if patch['!@#$c_index'] not in group_mapping:
                group_mapping[patch['!@#$c_index']] = count
            patch['group'] = group_mapping[patch['!@#$c_index']]

        count += 1


def unify(patches1, patches2, conflicts):
    unified_patches = [x for x in patches1+patches2
                       if 'take' not in x or ('take' in x and x['take'])]

    _assign_conflict_index(conflicts)
    _reassign_groups(unified_patches)
    unified_patches.sort(key=lambda x: (x['group'], x['path'][-1]))

    return unified_patches

