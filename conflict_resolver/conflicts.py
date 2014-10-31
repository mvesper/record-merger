from prettytable import PrettyTable
from utils import _is_super_path


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


def _handle_conflict(patch1, patch2, patches1, patches2,
                     conflicts, additional_info):
    if _is_conflict(patch1, patch2):
        if patch1['group'] is None or ('environment' in patch1 and patch1['environment'] == 'set'):
            # regular
            conflicts.append(([patch1], [patch2]))
        else:
            if 'conflicted' in patch1 and 'conflicted' in patch2:
                return

            # get groups
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
