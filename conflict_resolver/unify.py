def contains(patch, conflicts):
    for i, (patch1, patch2) in enumerate(conflicts):
        if patch == patch1 or patch == patch2:
            return i
    return None


def take_patches(patch1, patch2):
    # We will assume that we don't have to fix the indexes here...
    for i, (p1, p2) in enumerate(zip(patch1['patches'], patch2['patches'])):
        if i in patch1['take'] and i in patch2['take']:
            raise Exception("Can't take two conflicting patches")
        if p1 is not None and i in patch1['take'] and 'taken' not in patch1:
            yield p1
        if p2 is not None and i in patch2['take'] and 'taken' not in patch2:
            yield p2

    patch1['taken'] = patch2['taken'] = True


def unify(patches1, patches2, conflicts):
    
    for patch in patches1 + patches2:
        if 'taken' in patch:
            continue

        index = contains(patch, conflicts)
        if index is not None:
            for p in take_patches(*conflicts[index]):
                yield p
        else:
            for p in patch['patches']:
                yield p

"""
from copy import deepcopy
from patch_extractor.utils import delete_patch


def _assign_id(patches):
    id = 0
    for patch in patches:
        patch['!@#$id'] = id
        id += 1


def _assign_source(patches, source):
    for patch in patches:
        patch['!@#$source'] = source


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
                if (patch['!@#$source'], patch['group']) not in group_mapping:
                    group_mapping[(patch['!@#$source'], patch['group'])] = count
                patch['group'] = group_mapping[(patch['!@#$source'], patch['group'])]
            else:
                if patch['!@#$c_index'] not in group_mapping:
                    group_mapping[patch['!@#$c_index']] = count
                patch['group'] = group_mapping[patch['!@#$c_index']]

        count += 1

    return group_mapping



def _cleanup_patches(patches):
    for patch in patches:
        try:
            del patch['!@#$id']
        except KeyError:
            pass
        try:
            del patch['!@#$c_index']
        except KeyError:
            pass
        try:
            del patch['!@#$source']
        except KeyError:
            pass


def unify(patches1, patches2, conflicts):
    _assign_id(patches1+patches2)
    _assign_source(patches1, 1)
    _assign_source(patches2, 2)
    _assign_conflict_index(conflicts)

    copied_patches1 = deepcopy(patches1)
    copied_patches2 = deepcopy(patches2)

    for _patches1, _patches2 in conflicts:
        for patch1, patch2 in zip(_patches1, _patches2):
            try:
                if patch1 is None:
                    if not patch2['take']:
                        delete_patch(patch2, copied_patches2)
                elif patch2 is None:
                    if not patch1['take']:
                        delete_patch(patch1, copied_patches1)
                else:
                    if patch1['take'] == patch2['take'] == False:
                        delete_patch(patch1, copied_patches1)
                        delete_patch(patch2, copied_patches2)
                    elif patch1['take']:
                        delete_patch(patch2, copied_patches2,
                                     alter_group=False)
                    else:
                        delete_patch(patch1, copied_patches1,
                                     alter_group=False)
            except ValueError:
                pass

    unified_patches = copied_patches1 + copied_patches2

    _reassign_groups(unified_patches)
    unified_patches.sort(key=lambda x: (x['group'], x['path'][-1]))

    _cleanup_patches(patches1+patches2)

    return unified_patches
"""
