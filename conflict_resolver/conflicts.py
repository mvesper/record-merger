from prettytable import PrettyTable
from utils import _is_super_path

from itertools import product

from orderedset import OrderedSet


def _is_conflict(patch1, patch2):
    path1 = patch1['path']
    path2 = patch2['path']

    if not _is_super_path(path1[:-1], path2[:-1]) or not _is_super_path(path2[:-1], path1[:-1]):
        return False, OrderedSet()
    
    intersection = patch1['path'][-1].intersection(patch2['path'][-1])
    if intersection:
        return True, intersection
    elif _is_super_path(patch1['path'], patch2['path']):
        return True, intersection
    elif _is_super_path(patch2['path'], patch1['path']):
        return True, intersection
    else:
        return False, intersection


def _pad_patches(patch1, patch2, intersection):

    def ammend_patches(path, patch, intersection):
        if not path in intersection:
            if path < intersection[0]:
                patch['patches'].insert(0, None)
            else:
                patch['patches'].append(None)

    for path in patch1['path'][-1]:
        ammend_patches(path, patch2, intersection)
    for path in patch2['path'][-1]:
        ammend_patches(path, patch1, intersection)


def _handle_conflict(patch1, patch2, patches1, patches2):
    case, intersection = _is_conflict(patch1, patch2)
    if case:
        if intersection:
            _pad_patches(patch1, patch2, intersection)

        return (patch1, patch2)


def _get_conflicts(patches1, patches2, conflict_handler):
    # TODO: Improvable?
    for patch1, patch2 in product(patches1, patches2):
        yield conflict_handler(patch1, patch2, patches1, patches2)


def get_conflicts(patches1, patches2, conflict_handler=_handle_conflict):
    return (conflict for conflict
            in _get_conflicts(patches1, patches2, conflict_handler)
            if conflict is not None)


def print_conflicts(conflicts):
    
    def get_path(patch):
        if patch[1] != '':
            keys = patch[1].split('.') if isinstance(patch[1], str) else patch[1]
        else:
            keys = []
        keys = keys + [patch[2][0]] if patch[0] != 'change' else keys
        if keys == ['']:
            return ''
        return tuple(keys)

    def get_original(patch):
        if patch[0] == 'add':
            return ''
        elif patch[0] == 'remove':
            return patch[2][1]
        else:
            return patch[2][0]

    pt = PrettyTable(['INDEX',
                      'LEFT PATH',
                      'LEFT ACTION',
                      'LEFT VALUE',
                      'ORIGINAL',
                      'RIGHT VALUE',
                      'RIGHT ACTION',
                      'RIGHT PATH'])

    for i, (patch1, patch2) in enumerate(conflicts):
        path1, path2 = patch1['path'][-1], patch2['path'][-1]
        for index, _patch1, _patch2 in zip(path1.union(path2),
                                           patch1['patches'],
                                           patch2['patches']):
            if _patch1 is None:
                _patch1 = ('', '', ('', ''))
            if _patch2 is None:
                _patch2 = ('', '', ('', ''))

            pt.add_row([i,
                        get_path(_patch1),
                        _patch1[0],
                        _patch1[2][1],
                        get_original(_patch1),
                        _patch2[2][1],
                        _patch2[0],
                        get_path(_patch2)])
        pt.add_row(['', '', '', '', '', '', '', ''])

    print pt


"""
def _is_conflict(patch1, patch2):
    if patch1['path'] == patch2['path']:
        return True
    elif _is_super_path(patch1['path'], patch2['path']):
        return True
    elif _is_super_path(patch2['path'], patch1['path']):
        return True
    else:
        return False


def _get_patch_group(patch, patches):
    group = [p for p in patches
             if p['path'][:-1] == patch['path'][:-1]
             and p['group'] == patch['group']]
    # TODO: This might potential fail in some cases...
    # What happens in case of multiple deletes with the same path, values?
    return group.index(patch), group


def _get_none_list(count):
    return [None for _ in range(count)]


def _pad_patch_groups(patch1, patch2, patches1, patches2):
    i1, patch1_group = _get_patch_group(patch1, patches1)
    i2, patch2_group = _get_patch_group(patch2, patches2)

    # prepend, append Nones
    patch1_group_len = len(patch1_group)
    patch2_group_len = len(patch2_group)

    patch1_group = (_get_none_list(i2-i1) +
                    patch1_group +
                    _get_none_list((patch2_group_len-i2) -
                                   (patch1_group_len-i1)))
    patch2_group = (_get_none_list(i1-i2) +
                    patch2_group +
                    _get_none_list((patch1_group_len-i1) -
                                   (patch2_group_len-i2)))

    return patch1_group, patch2_group


def _is_set_environment(patch):
    return (patch['group'] is None or
            ('environment' in patch and patch['environment'] == 'set'))


def _handle_conflict(patch1, patch2, patches1, patches2,
                     conflicts, additional_info):
    if _is_conflict(patch1, patch2):
        if _is_set_environment(patch1):
            # regular
            conflicts.append(([patch1], [patch2]))
        else:
            if 'conflicted' in patch1 and 'conflicted' in patch2:
                return

            patch1_group, patch2_group = _pad_patch_groups(patch1,
                                                           patch2,
                                                           patches1,
                                                           patches2)

            conflicts.append((patch1_group, patch2_group))

            for p in patch1_group+patch2_group:
                try:
                    p['conflicted'] = True
                except TypeError:
                    pass


def get_conflicts(patches1, patches2,
                  additional_info=None,
                  conflict_handler=_handle_conflict):
    conflicts = []

    for patch1 in patches1:
        for patch2 in patches2:
            conflict_handler(patch1, patch2, patches1, patches2,
                             conflicts, additional_info)

    return conflicts


def print_conflicts(conflicts):
    pt = PrettyTable(['INDEX',
                      'LEFT PATH',
                      'LEFT ACTION',
                      'LEFT VALUE',
                      'ORIGINAL',
                      'RIGHT VALUE',
                      'RIGHT ACTION',
                      'RIGHT PATH'])

    for i, (patches1, patches2) in enumerate(conflicts):
        if len(patches1) == len(patches2) == 1:
            patch1 = patches1[0]
            patch2 = patches2[0]
            pt.add_row([i,
                        patch1['path'],
                        patch1['action'],
                        patch1['value']['to'],
                        patch1['value']['from'],
                        patch2['value']['to'],
                        patch2['action'],
                        patch2['path']])
        else:
            def val(key):
                return lambda x: x[key] if x else ''

            def val2(key1, key2):
                return lambda x: x[key1][key2] if x else ''

            def val3(key1, key2):
                return lambda x, y: x[key1][key2] if x else y[key1][key2]

            def lines(_lines):
                return '\n'.join(map(str, _lines))

            patch1_paths = lines(map(val('path'), patches1))
            patch1_actions = lines(map(val('action'), patches1))
            patch1_values = lines(map(val2('value', 'to'), patches1))
            originals = lines(map(val3('value', 'from'), patches1, patches2))
            patch2_paths = lines(map(val('path'), patches2))
            patch2_actions = lines(map(val('action'), patches2))
            patch2_values = lines(map(val2('value', 'to'), patches2))

            pt.add_row([i,
                        patch1_paths,
                        patch1_actions,
                        patch1_values,
                        originals,
                        patch2_values,
                        patch2_actions,
                        patch2_paths])

    print pt
"""
