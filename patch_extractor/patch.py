def get_containing(old_obj, path):
    containing = old_obj
    for p in path[:-1]:
        try:
            containing = containing.__getitem__(p)
        except AttributeError:
            containing = getattr(containing, p)
    return containing


def add(old_obj, path, value):
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


def remove(old_obj, path, value):
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


def change(old_obj, path, value):
    value = value[1]
    insert_to = get_containing(old_obj, path)

    try:
        insert_to[path[-1]] = value
    except AttributeError:
        setattr(insert_to, path[-1], value)

    return 0


def shift(patches, index, _path, _shift):
    _action, latest_path, _ = patches[index-1]
    consecutive = True
    latest_path = latest_path[-1]
    for i, (action, path, value) in enumerate(patches[index:]):
        if _path[:-1] == path[:-1]:
            if action == _action == 'add':
                if not path[-1] == latest_path+1:
                    consecutive = False
            elif action == _action == 'remove':
                if not path[-1] == latest_path:
                    consecutive = False
            else:
                consecutive = False

            if not consecutive:
                new_path = _path[:-1]+(path[-1]+_shift,)
                patches[index+i] = (action, new_path, value)

            latest_path = path[-1]


def patch(obj, patches):
    actions = {'add': add,
               'change': change,
               'remove': remove}

    for i, (action, path, value) in enumerate(patches):
        _shift = actions[action](obj, path, value)
        if _shift:
            shift(patches, i+1, path, _shift)

    return obj

