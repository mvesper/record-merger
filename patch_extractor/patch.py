from copy import deepcopy


def nothing(*_):
    pass


def get_containing(old_obj, path):
    containing = old_obj
    for p in path[:-1]:
        try:
            containing = containing.__getitem__(p)
        except AttributeError:
            containing = getattr(containing, p)
    return containing


def add(old_obj, patch):
    path = patch['path']
    value = patch['value']['to']
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


def remove(old_obj, patch):
    path = patch['path']
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


def change(old_obj, patch):
    path = patch['path']
    value = patch['value']['to']
    insert_to = get_containing(old_obj, path)

    try:
        insert_to[path[-1]] = value
    except AttributeError:
        setattr(insert_to, path[-1], value)

    return 0


def move(old_obj, patch):
    old_obj_action = patch['move']['old_action']
    new_obj_action = patch['move']['new_action']

    OLD_OBJ_ACTIONS[old_obj_action](old_obj, patch)
    if patch['group'] is not None and patch['move']['old_action'] == 'add':
        tmp_path_end = patch['move']['moved_from'][-1]+1
    else:
        tmp_path_end = patch['move']['moved_from'][-1]

    tmp_patch = {'path': patch['move']['moved_from'][:-1]+(tmp_path_end,)}

    NEW_OBJ_ACTIONS[new_obj_action](old_obj, tmp_patch)


def shift(original_patches, patches, index, _path, _shift):
    last_group = original_patches[index-1]['group']

    if last_group is not None:
        for i, patch in enumerate(original_patches[index:]):
            if _path[:-1] == patch['path'][:-1]:
                if patch['group'] != last_group:
                    if patches[index+i]['path'][-1] > patches[index]['path'][-1]
                        # This way the order of groups is not important
                        patches[index+i]['path'] = patches[index+i]['path'][:-1] + (patches[index+i]['path'][-1]+_shift,)


def patch(obj, _patches):
    obj = deepcopy(obj)
    patches = deepcopy(_patches)

    for i, patch in enumerate(patches):
        _shift = ACTIONS[patch['action']](obj, patch)
        if _shift:
            shift(_patches, patches, i+1, patch['path'], _shift)

    return obj


ACTIONS = {'add': add,
           'change': change,
           'remove': remove,
           'move': move}
OLD_OBJ_ACTIONS = {'add': add, 'change': change}
NEW_OBJ_ACTIONS = {'remove': remove, 'dont_remove': nothing}
