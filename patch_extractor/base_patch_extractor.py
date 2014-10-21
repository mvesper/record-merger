from copy import deepcopy

from dictdiffer import DictDiffer

from json import dumps
from difflib import SequenceMatcher


class BasePatchExtractor(object):
    def __init__(self,
                 old_obj, new_obj,
                 previous_old_path=(), previous_new_path=(),
                 patch_extractors=[]):
        self.patches = []
        self.previous_old_path = previous_old_path
        self.previous_new_path = previous_new_path

    def _add_patch(action, path, value):
        _path = self.previous_old_path + (path,)
        if hasattr(value, '__iter__'):
            _value = tuple(map(deepcopy, value))
        else:
            _value = deepcopy(value)
        self.patches.append((action, (_path,), _value))


    def _stringify(self, var):
        try:
            return dumps(var)
        except TypeError:
            return dumps(var.__dict__)

    def _find_moved_parts(self, patches):
        for patch1 in patches:
            for patch2 in patches:
                val1_str = stringify(patch1[2])
                val2_str = stringify(patch2[2])
                s = SequenceMatcher(None, val1_str, val2_str)
                if s.ratio() > 0.8:
                    print 'Probably moved'
                    print patch1
