from os import listdir
from os.path import (isfile, join)


class WildcardDict(dict):
    '''
    *:  wildcard for everything that follows
    +:  wildcard for anything on the same path level
    '''
    def __init__(self):
        super(WildcardDict, self).__init__()
        self.star_keys = set()
        self.plus_keys = set()

    def __getitem__(self, key):
        try:
            return super(WildcardDict, self).__getitem__(key)
        except KeyError:
            if key[:-1] in self.plus_keys:
                return super(WildcardDict, self).__getitem__(key[:-1]+('+',))
            for _key in [key[:-i] for i in range(1, len(key)+1)]:
                if _key in self.star_keys:
                    return super(WildcardDict, self).__getitem__(_key+('*',))
            raise KeyError

    def __setitem__(self, key, value):
        super(WildcardDict, self).__setitem__(key, value)

        if key[-1] == '+':
            self.plus_keys.add(key[:-1])
        if key[-1] == '*':
            self.star_keys.add(key[:-1])

    def query_path(self, key):
        if key in self:
            return key
        if key[:-1] in self.plus_keys:
            return key[:-1]+('+',)
        for _key in [key[:-i] for i in range(1, len(key)+1)]:
            if _key in self.star_keys:
                return _key+('*',)

        raise KeyError


def get_filenames_from_directory(dirname, _filter=''):
    return [join(dirname, f) for f in listdir(dirname)
            if isfile(join(dirname, f)) and _filter in f]

