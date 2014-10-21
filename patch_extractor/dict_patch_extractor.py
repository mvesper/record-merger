from copy import deepcopy

from dictdiffer import DictDiffer


class DictPatchExtractor(object):
    def __init__(self,
                 old_obj, new_obj,
                 previous_path=(), previous_new_path=(),
                 patch_extractors=[]):
        self.patches = []
        dict_diff = DictDiffer(new_obj, old_obj)

        for addition_key in dict_diff.added():
            action = 'add'
            path = previous_path + (addition_key,)
            value = deepcopy(new_obj[addition_key])
            self.patches.append((action, path, value))

        for removal_key in dict_diff.removed():
            action = 'remove'
            path = previous_path + (removal_key,)
            value = deepcopy(old_obj[removal_key])
            self.patches.append((action, path, value))

        for change_key in dict_diff.changed():
            for patch_extractor in patch_extractors:
                if patch_extractor.is_applicable(old_obj[change_key],
                                                 new_obj[change_key]):
                    extractor = patch_extractor(old_obj[change_key],
                                                new_obj[change_key],
                                                previous_path+(change_key,),
                                                previous_new_path+(change_key,),
                                                patch_extractors)
                    self.patches.extend(extractor.patches)
                    break
            else:
                action = 'change'
                path = previous_path + (change_key,)
                value = (deepcopy(old_obj[change_key]),
                         deepcopy(new_obj[change_key]))
                self.patches.append((action, path, value))

    @classmethod
    def is_applicable(cls, old_obj, new_obj):
        return isinstance(new_obj, dict) and isinstance(old_obj, dict)

