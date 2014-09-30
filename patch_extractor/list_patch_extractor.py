from copy import deepcopy

from difflib import SequenceMatcher

from data import Patch
from actions import insert_action, delete_action, replace_action


class ListPatchExtractor:
    # The problem with list is that the order is important -> insert/delete in chunks
    # TODO: It's tuple, not tupel
    def __init__(self,
                 old_obj, new_obj,
                 previous_path=[], previous_new_path=[],
                 patch_extractors=[]):
        self.patches = []
        sequence = SequenceMatcher(None, self.tuple_it(old_obj),
                                   self.tuple_it(new_obj))

        for tupel in sequence.get_opcodes():
            if tupel[0] == 'insert':
                '''
                This groups the changes in one patch
                patch = Patch()
                patch.path.extend(previous_path)
                patch.path.append(tupel[1])
                values = []
                for i, new_path in enumerate(range(tupel[3], tupel[4])):
                    values.append(deepcopy(new_obj[new_path]))
                patch.value = values
                patch.action = insert_action
                self.patches.append(patch)
                '''
                for i, new_path in enumerate(range(tupel[3], tupel[4])):
                    patch = Patch()
                    patch.path.extend(previous_path)
                    patch.path.append(tupel[1]+i)
                    patch.value = deepcopy(new_obj[new_path])
                    patch.action = insert_action
                    self.patches.append(patch)
            elif tupel[0] == 'replace':
                for path, new_path in zip(range(tupel[1], tupel[2]),
                                              range(tupel[3], tupel[4])):
                    for patch_extractor in patch_extractors:
                        if patch_extractor.is_applicable(old_obj[new_path],
                                                         new_obj[path]):
                            _new_path = previous_new_path+[new_path],
                            _path = previous_path+[path],
                            extractor = patch_extractor(old_obj[new_path],
                                                        new_obj[path],
                                                        _path,
                                                        _new_path,
                                                        patch_extractors)
                            self.patches.extend(extractor.patches)
                            break
                    else:
                        patch = Patch()
                        patch.path.extend(previous_path)
                        patch.path.append(path)
                        patch.value = deepcopy(new_obj[new_path])
                        patch.action = replace_action
                        self.patches.append(patch)
            elif tupel[0] == 'delete':
                '''
                patch = Patch()
                patch.path.extend(previous_path)
                patch.path.append(tupel[1])
                patch.value = tupel[2] - tupel[1]
                patch.action = delete_action
                self.patches.append(patch)
                '''
                path = tupel[1]
                for _ in range(tupel[1], tupel[2]):
                    patch = Patch()
                    patch.path.extend(previous_path)
                    patch.path.append(path)
                    patch.action = delete_action
                    self.patches.append(patch)
            else:
                continue

    @classmethod
    def is_applicable(cls, old_obj, new_obj):
        if isinstance(new_obj, list) and isinstance(old_obj, list):
            return True
        return False

    def tuple_it(self, t):
        return tuple(map(self.tuple_it, t)) if isinstance(t, list) else t

