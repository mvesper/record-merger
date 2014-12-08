from itertools import starmap


def _find_conflicting_path(patch1, patch2):
    p1p = patch1['path'][:-1] + (patch1['path'][-1][0],)
    p2p = patch2['path'][:-1] + (patch2['path'][-1][0],)

    # This returns the shortest path
    return p1p if len(p1p) < len(p2p) else p2p


def _auto_resolve(patch1, patch2):
    if any(starmap(lambda x, y: x != y, zip(patch1['patches'],
                                            patch2['patches']))):
        return False
    patch1['take'] = range(len(patch1['patches']))
    patch2['take'] = []

    return True


def resolve(patches1, patches2, conflicts, actions,
            additional_info=None,
            auto_resolve=_auto_resolve,
            conflicting_path_method=_find_conflicting_path):

    def consecutive_slices(iterable):
        return (iterable[:i] for i in reversed(range(1, len(iterable)+1)))

    unresolved_conflicts = []
    for patch1, patch2 in conflicts:
        conflict_path = conflicting_path_method(patch1, patch2)

        if auto_resolve and auto_resolve(patch1, patch2):
            continue
        # Let's do some cascading here
        for sub_path in consecutive_slices(conflict_path):
            print sub_path
            try:
                if actions[sub_path](patch1, patch2, patches1, patches2,
                                     additional_info):
                    break
            except KeyError:
                pass
        else:
            # The conflict could not be resolved
            unresolved_conflicts.append((patch1, patch2))

    return unresolved_conflicts


"""
def _find_conflicting_path(patches1, patches2):
    for patch in patches1:
        if patch is not None:
            p1p = patch['path']
            break
    for patch in patches2:
        if patch is not None:
            p2p = patch['path']
            break

    # This returns the shortest path
    return p1p if len(p1p) < len(p2p) else p2p


def _auto_resolve(patches1, patches2):
    # In case everything is the same in a conflicts, it's ok
    for patch1, patch2 in zip(patches1, patches2):
        try:
            if any(map(lambda x: patch1[x] != patch2[x],
                       ['path', 'action', 'value'])):
                break
        except TypeError:
            break
    else:
        for patch in patches1:
            patch['take'] = True
        for patch in patches2:
            patch['take'] = False
        return True

    return False


def resolve(patches1, patches2, conflicts, actions,
            additional_info=None,
            auto_resolve=_auto_resolve,
            conflicting_path_method=_find_conflicting_path):
    unresolved_conflicts = []
    for _patches1, _patches2 in conflicts:
        conflict_path = conflicting_path_method(patches1, patches2)

        if auto_resolve and auto_resolve(_patches1, _patches2):
            continue
        # Let's do some cascading here
        for sub_path in [conflict_path[:i] for i in
                         range(len(conflict_path), -1, -1)]:
            try:
                if actions[sub_path](_patches1, _patches2, patches1, patches2, additional_info):
                    break
            except KeyError:
                pass
        else:
            # The conflict could not be resolved
            unresolved_conflicts.append((_patches1, _patches2))

    return unresolved_conflicts
"""
