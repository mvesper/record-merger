from copy import deepcopy

from dictdiffer import DictDiffer

from data import Patch
from actions import insert_action, delete_action, replace_action


class ObjectPatchExtractor:
    def __init__(self,
                 old_obj, new_obj,
                 previous_path=[], previous_new_path=[],
                 patch_extractors=[]):
        self.patches = []

        old_obj = old_obj.__dict__
        new_obj = new_obj.__dict__

        dict_diff = DictDiffer(new_obj, old_obj)

        for addition_key in dict_diff.added():
            patch = Patch()
            patch.path.extend(previous_path)
            patch.path.append(addition_key)
            patch.value = deepcopy(new_obj[addition_key])
            patch.action = insert_action
            self.patches.append(patch)

        for removal_key in dict_diff.removed():
            patch = Patch()
            patch.path.extend(previous_path)
            patch.path.append(removal_key)
            patch.action = delete_action
            self.patches.append(patch)

        for change_key in dict_diff.changed():
            for patch_extractor in patch_extractors:
                if patch_extractor.is_applicable(old_obj[change_key],
                                                 new_obj[change_key]):
                    extractor = patch_extractor(old_obj[change_key],
                                                new_obj[change_key],
                                                previous_path+[change_key],
                                                previous_new_path+[change_key],
                                                patch_extractors)
                    self.patches.extend(extractor.patches)
                    break
            else:
                patch = Patch()
                patch.path.extend(previous_path)
                patch.path.append(change_key)
                patch.value = deepcopy(new_obj[change_key])
                patch.action = replace_action
                self.patches.append(patch)

    @classmethod
    def is_applicable(cls, old_obj, new_obj):
        if isinstance(new_obj, object) and isinstance(old_obj, object):
            return True
        return False

