from itertools import izip_longest
from copy import deepcopy

from difflib import SequenceMatcher


class ListPatchExtractor:
    def __init__(self,
                 old_obj, new_obj,
                 previous_path=(), previous_new_path=(),
                 patch_extractors=[]):
        self.patches = []
        sequence = SequenceMatcher(None, self.make_hashable(old_obj),
                                   self.make_hashable(new_obj))

        for _tuple in sequence.get_opcodes():
            if _tuple[0] == 'insert':
                for i, new_path in enumerate(range(_tuple[3], _tuple[4])):
                    action = 'add'
                    path = previous_path + (_tuple[1]+i,)
                    value = deepcopy(new_obj[new_path])
                    self.patches.append((action, path, value))

            elif _tuple[0] == 'replace':
                old_range = range(_tuple[1], _tuple[2])
                new_range = range(_tuple[3], _tuple[4])
                for old_path, new_path in izip_longest(old_range, new_range):
                    if old_path and new_path:
                        for patch_extractor in patch_extractors:
                            _old_obj = old_obj[old_path]
                            _new_obj = new_obj[new_path]
                            if patch_extractor.is_applicable(_old_obj,
                                                             _new_obj):
                                _new_path = previous_new_path+(new_path,),
                                _path = previous_path+(old_path,),
                                extractor = patch_extractor(_old_obj,
                                                            _new_obj,
                                                            _path,
                                                            _new_path,
                                                            patch_extractors)
                                self.patches.extend(extractor.patches)
                                break
                        else:
                            action = 'change'
                            path = previous_path + (old_path,)
                            value = (deepcopy(old_obj[old_path]),
                                     deepcopy(new_obj[new_path]))
                            self.patches.append((action, path, value))
                    elif new_path:
                        action = 'add'
                        path = previous_path + (last_old_path+1,)
                        value = deepcopy(new_obj[new_path])
                        self.patches.append((action, path, value))
                    elif old_path:
                        action = 'remove'
                        path = previous_path + (old_path,)
                        value = deepcopy(old_obj[old_path])
                        self.patches.append((action, path, value))

                    if old_path:
                        last_old_path = old_path
                    else:
                        last_old_path += 1

            elif _tuple[0] == 'delete':
                path = _tuple[1]
                for removal_key in range(_tuple[1], _tuple[2]):
                    action = 'remove'
                    path = previous_path + (path,)
                    value = deepcopy(old_obj[removal_key])
                    self.patches.append((action, path, value))

            else:
                continue

    @classmethod
    def is_applicable(cls, old_obj, new_obj):
        return isinstance(new_obj, list) and isinstance(old_obj, list)

    def make_hashable(self, t):
        if isinstance(t, (set, list)):
            return tuple(map(self.make_hashable, t))
        elif isinstance(t, dict):
            return hash(repr(sorted(t.items())))
        else:
            return t
