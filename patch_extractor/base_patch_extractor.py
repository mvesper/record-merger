from copy import deepcopy

from json import dumps
from difflib import SequenceMatcher


class BasePatchExtractor(object):
    def __init__(self,
                 old_obj, new_obj,
                 previous_old_path=(), previous_new_path=(),
                 patch_extractors=[],
                 moved_patches_similarity=0.8):
        self.patches = []
        self.old_obj = old_obj
        self.new_obj = new_obj
        self.previous_old_path = previous_old_path
        self.previous_new_path = previous_new_path
        self.patch_extractors = patch_extractors
        self.similarity = moved_patches_similarity

    def _add_patch(self, action, path, value, to_value=None, group=None):
        _path = self.previous_old_path + (path,)
        if action == 'change':
            _value = (deepcopy(value), deepcopy(to_value))
        else:
            _value = deepcopy(value)
        self.patches.append((action, _path, _value, group))

    def _try_patch_extractors(self, old_key, new_key):
        for patch_extractor in self.patch_extractors:
            if patch_extractor.is_applicable(self.old_obj[old_key],
                                             self.new_obj[new_key]):
                extractor = patch_extractor(self.old_obj[old_key],
                                            self.new_obj[new_key],
                                            self.previous_old_path+(old_key,),
                                            self.previous_new_path+(new_key,),
                                            self.patch_extractors)
                self.patches.extend(extractor.patches)

                return True

        return False

    def _stringify(self, var):
        try:
            return dumps(var)
        except TypeError:
            return dumps(var.__dict__)

    def _estimate_similarity(self, value1, value2):
        val1 = self._stringify(value1)
        val2 = self._stringify(value2)
        s = SequenceMatcher(None, val1, val2)
        return s.ratio()

    def _create_move_patch(self, patches, patch1, patch2, i, j,
                           comp_val1, comp_val2, action1, action2):
        _similarity = self._estimate_similarity(comp_val1, comp_val2)
        if _similarity > self.similarity:
            patches[i] = ('move',
                          patch1[1],
                          patch1[2],
                          patch1[3],
                          (patch2[1], action1, action2))
            patches[j] = ('cleared',)

    def _find_moved_parts(self):
        patches = self.patches[:]
        for i, patch1 in enumerate(patches):
            for j, patch2 in enumerate(patches):
                if patch1 == patch2:
                    continue

                if patch1[0] == 'move' or patch2[0] == 'move':
                    continue

                if patch1[0] == 'cleared' or patch2[0] == 'cleared':
                    continue

                if patch1[0] == patch2[0] == 'remove':
                    continue

                if patch1[0] == patch2[0] == 'add':
                    continue

                if patch1[0] == 'add' and patch2[0] == 'remove':
                    self._create_move_patch(patches, patch1, patch2, i, j, patch1[2], patch2[2], 'add', 'remove')

                if patch1[0] == 'remove' and patch2[0] == 'add':
                    self._create_move_patch(patches, patch2, patch1, j, i, patch2[2], patch1[2], 'add', 'remove')

                if patch1[0] == 'change' and patch2[0] == 'remove':
                    self._create_move_patch(patches, patch1, patch2, i, j, patch1[2][1], patch2[2], 'change', 'remove')

                if patch1[0] == 'remove' and patch2[0] == 'change':
                    self._create_move_patch(patches, patch2, patch1, j, i, patch2[2][1], patch1[2], 'change', 'remove')

                if patch2[0] == 'change' and patch1[0] == 'change':
                    _similarity1 = self._estimate_similarity(patch1[2][0], patch2[2][1])
                    _similarity2 = self._estimate_similarity(patch1[2][1], patch2[2][0])
                    if _similarity1 > self.similarity and _similarity2 > self.similarity:
                        patches[i] = ('move',
                                      patch1[1],
                                      patch1[2],
                                      patch1[3],
                                      (patch2[1], 'change', 'dont_remove'))
                        patches[j] = ('move',
                                      patch2[1],
                                      patch2[2],
                                      patch2[3],
                                      (patch1[1], 'change', 'dont_remove'))

                return filter(lambda x: x[0] != 'cleared', patches)
                
