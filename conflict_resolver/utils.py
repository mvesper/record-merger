from itertools import izip_longest


def _is_super_path(path1, path2):
    return all(map(lambda x: x[0] == x[1] or x[0] is None,
                   izip_longest(path1, path2)))

