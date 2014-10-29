from itertools import izip_longest
from difflib import SequenceMatcher

from base_patch_extractor import BasePatchExtractor
from utils import KeyLimit


class ListPatchExtractor(BasePatchExtractor):
    def __init__(self,
                 old_obj, new_obj,
                 previous_path=(), previous_new_path=(),
                 patch_extractors=[],
                 key_limits=KeyLimit(),
                 find_moved_patches=False,
                 moved_patches_similarity=0.8):

        super(ListPatchExtractor, self).__init__(old_obj, new_obj,
                                                 previous_path,
                                                 previous_new_path,
                                                 patch_extractors,
                                                 key_limits,
                                                 moved_patches_similarity)

        sequence = SequenceMatcher(None, self.make_hashable(old_obj),
                                   self.make_hashable(new_obj))

        group = 0

        for _tuple in sequence.get_opcodes():
            if _tuple[0] == 'insert':
                for i, new_path in enumerate(range(_tuple[3], _tuple[4])):
                    if not self._try_patch_extractors_for_ungrouping(_tuple[1]+i):
                        self._add_patch('add', _tuple[1]+i, None, new_obj[new_path], group)

            elif _tuple[0] == 'replace':
                old_range = range(_tuple[1], _tuple[2])
                new_range = range(_tuple[3], _tuple[4])

                for old_path, new_path in izip_longest(old_range, new_range):
                    if old_path is not None and new_path is not None:
                        if not self._try_patch_extractors(old_path, new_path):
                            self._add_patch('change', old_path,
                                            old_obj[old_path],
                                            new_obj[new_path],
                                            group)
                        
                        last_old_path = old_path
                    elif new_path is not None:
                        if not self._try_patch_extractors_for_ungrouping(last_old_path+1):
                            self._add_patch('add', last_old_path+1, None,
                                            new_obj[new_path], group)
                        last_old_path += 1
                    elif old_path is not None:
                        self._add_patch('remove', last_old_path+1, old_obj[old_path], None, group)

            elif _tuple[0] == 'delete':
                path = _tuple[1]
                for removal_key in range(_tuple[1], _tuple[2]):
                    self._add_patch('remove', path, old_obj[removal_key], None, group)

            group += 1

        if find_moved_patches:
            self.patches = self._find_moved_parts()

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
