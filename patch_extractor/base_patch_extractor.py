from copy import deepcopy

from json import dumps
from difflib import SequenceMatcher

from utils import KeyLimit


class BasePatchExtractor(object):
    def __init__(self,
                 old_obj, new_obj,
                 previous_old_path=(), previous_new_path=(),
                 patch_extractors=[],
                 key_limits=KeyLimit(),
                 moved_patches_similarity=0.8):
        self.patches = []
        self.old_obj = old_obj
        self.new_obj = new_obj
        self.previous_old_path = previous_old_path
        self.previous_new_path = previous_new_path
        self.patch_extractors = patch_extractors
        self.key_limits = key_limits
        self.similarity = moved_patches_similarity

    def _add_patch(self, action, path, from_value, to_value, group=None):
        patch = self._create_patch(action, path, from_value, to_value, group)
        self.patches.append(patch)

    def _create_patch(self, action, path, from_value, to_value, group=None):
        patch = {'action': action,
                 'path': self.previous_old_path + (path,),
                 'value': {'from': from_value, 'to': to_value},
                 'group': group}

        return patch

    def _try_patch_extractors(self, old_key, new_key):
        if self.key_limits.key_is_limit(self.previous_old_path+(old_key,)):
            return False

        for patch_extractor in self.patch_extractors:
            if patch_extractor.is_applicable(self.old_obj[old_key],
                                             self.new_obj[new_key]):
                extractor = patch_extractor(self.old_obj[old_key],
                                            self.new_obj[new_key],
                                            self.previous_old_path+(old_key,),
                                            self.previous_new_path+(new_key,),
                                            self.patch_extractors,
                                            self.key_limits)
                self.patches.extend(extractor.patches)

                return True

        return False

    def _try_patch_extractors_for_ungrouping(self, key, group=None):
        if self.key_limits.key_is_limit(self.previous_old_path+(key,)):
            return False

        new_obj = self.new_obj[key]
        old_obj = new_obj.__class__()
        for patch_extractor in self.patch_extractors:
            if patch_extractor.is_applicable(old_obj, new_obj):
                extractor = patch_extractor(old_obj,
                                            new_obj,
                                            self.previous_old_path+(key,),
                                            self.previous_new_path+(key,),
                                            self.patch_extractors,
                                            self.key_limits)
                self.patches.append(self._create_patch('add', key, None, old_obj, group))
                self.patches.extend(extractor.patches)

                return True

        return False

    # MOVED PART
    def _stringify(self, var):
        try:
            return dumps(var, sort_keys=True)
        except TypeError:
            return dumps(var.__dict__, sort_keys=True)

    def _estimate_similarity(self, value1, value2):
        val1 = self._stringify(value1)
        val2 = self._stringify(value2)
        s = SequenceMatcher(None, val1, val2)
        return s.ratio()
    
    def _create_move_patch(self, patch1, patch2, comp_val1, comp_val2, action1, action2):
        _similarity = self._estimate_similarity(comp_val1, comp_val2)
        if _similarity > self.similarity:
            patch1['action'] = 'move'
            patch1['move'] = {'moved_from': patch2['path'],
                              'old_action': action1,
                              'new_action': action2}
            patch2['cleared'] = 1


    def _find_moved_parts(self):
        patches = self.patches[:]
        for i, patch1 in enumerate(patches):
            for j, patch2 in enumerate(patches):
                if patch1 == patch2:
                    continue

                if patch1['action'] == 'move' or patch2['action'] == 'move':
                    continue

                if 'cleared' in patch1 or 'cleared' in patch2:
                    continue

                if patch1['action'] == patch2['action'] == 'remove':
                    continue

                if patch1['action'] == patch2['action'] == 'add':
                    continue

                if patch1['action'] == 'add' and patch2['action'] == 'remove':
                    self._create_move_patch(patch1, patch2, patch1['value']['to'], patch2['value']['from'], 'add', 'remove')

                if patch1['action'] == 'remove' and patch2['action'] == 'add':
                    self._create_move_patch(patch2, patch1, patch2['value']['to'], patch1['value']['from'], 'add', 'remove')

                if patch1['action'] == 'change' and patch2['action'] == 'remove':
                    self._create_move_patch(patch1, patch2, patch1['value']['to'], patch2['value']['from'], 'change', 'remove')

                if patch1['action'] == 'remove' and patch2['action'] == 'change':
                    self._create_move_patch(patch2, patch1, patch2['value']['to'], patch1['value']['from'], 'change', 'remove')

                if patch2['action'] == 'change' and patch1['action'] == 'change':
                    _similarity1 = self._estimate_similarity(patch1['value']['from'], patch2['value']['to'])
                    _similarity2 = self._estimate_similarity(patch1['value']['to'], patch2['value']['from'])
                    if _similarity1 > self.similarity and _similarity2 > self.similarity:
                        patch1['action'] = 'move'
                        patch1['move'] = {'moved_from': patch2['path'],
                                          'old_action': 'change',
                                          'new_action': 'dont_remove'}

                        patch2['action'] = 'move'
                        patch2['move'] = {'moved_from': patch1['path'],
                                          'old_action': 'change',
                                          'new_action': 'dont_remove'}

                return filter(lambda x: 'cleared' not in x, patches)
                
