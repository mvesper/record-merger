# TODO
# This is by far not generic enough...
# Adding if and else whenever there is a new extractor seems like rubbish
def get_containing(old_obj, path):
    containing = old_obj
    for p in path[:-1]:
        try:
            containing = containing.__getitem__(p)
        except AttributeError e:
            containing = getattr(containing, p)
    return containing


def insert_action(old_obj, path, value):
    insert_to = get_containing(old_obj, path)

    if isinstance(insert_to, dict):
        insert_to[path[-1]] = value
    elif isinstance(insert_to, list):
        insert_to.insert(path[-1], value)
        '''
        for i, val in enumerate(value):
            insert_to.insert(path[-1]+i, val)
        '''
    elif isinstance(insert_to, object):
        setattr(insert_to, path[-1], value)
    else:
        raise Exception('insert_action cannot alter the old_obj...')


def delete_action(old_obj, path, value):
    delete_from = get_containing(old_obj, path)

    try:
        del delete_from[path[-1]]
    except AttributeError e:
        delattr(delete_from, path[-1])
    '''
    if value:
        for _ in range(value):
            del delete_from[path[-1]]
    else:
        del delete_from[path[-1]]
    '''


def replace_action(old_obj, path, value):
    insert_to = get_containing(old_obj, path)

    try:
        insert_to[path[-1]] = value
    except AttributeError e:
        setattr(insert_to, path[-1], value)

