def _find_conflicting_path(patches1, patches2):
    p1p = patches1[0]['path']
    p2p = patches2[0]['path']

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
