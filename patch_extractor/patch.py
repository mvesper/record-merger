from copy import deepcopy


def get_containing(old_obj, path):
    containing = old_obj
    for p in path[:-1]:
        try:
            containing = containing.__getitem__(p)
        except AttributeError:
            containing = getattr(containing, p)
    return containing


def add(old_obj, path, value, rest):
    insert_to = get_containing(old_obj, path)

    if isinstance(insert_to, dict):
        insert_to[path[-1]] = value
        return 0
    elif isinstance(insert_to, list):
        insert_to.insert(path[-1], value)
        return 1
    elif isinstance(insert_to, object):
        setattr(insert_to, path[-1], value)
        return 0
    else:
        raise Exception('insert_action cannot alter the old_obj...')


def remove(old_obj, path, value, rest):
    delete_from = get_containing(old_obj, path)

    if isinstance(delete_from, dict):
        del delete_from[path[-1]]
        return 0
    elif isinstance(delete_from, list):
        del delete_from[path[-1]]
        return -1
    elif isinstance(delete_from, object):
        delattr(delete_from, path[-1])
        return 0
    else:
        raise Exception('could not delete value')


def change(old_obj, path, value, rest):
    value = value[1]
    insert_to = get_containing(old_obj, path)

    try:
        insert_to[path[-1]] = value
    except AttributeError:
        setattr(insert_to, path[-1], value)

    return 0


def move(old_obj, path, value, rest):
    old_obj_actions = {'add': add, 'change': change}
    new_obj_actions = {'remove': remove, 'dont_remove': nothing}

    old_obj_action = rest[1][1]
    new_obj_action = rest[1][2]

    del_path = rest[1][0]

    old_obj_actions[old_obj_action](old_obj, path, value, rest)
    new_obj_actions[new_obj_action](old_obj, del_path, value, rest)


def shift(original_patches, patches, index, _path, _shift):
    last_group = original_patches[index-1][3]

    if last_group is not None:
        for i, (action, path, value, group) in enumerate(original_patches[index:]):
            if _path[:-1] == path[:-1]:
                if group != last_group:
                    p = (patches[index+i][1][-1]+_shift,)
                    new_path = _path[:-1]+p
                    patches[index+i] = (action, new_path, value, group)


def nothing(*_):
    pass


def unpack(action, path, value, *rest):
    return (action, path, value, rest)


def patch(obj, _patches):
    actions = {'add': add,
               'change': change,
               'remove': remove,
               'move': move}

    obj = deepcopy(obj)
    patches = deepcopy(_patches)

    for i, (action, path, value, rest) in enumerate(map(lambda x: unpack(*x), patches)):
        _shift = actions[action](obj, path, value, rest)
        if _shift:
            shift(_patches, patches, i+1, path, _shift)

    return obj

