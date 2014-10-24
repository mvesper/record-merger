from dictdiffer import DictDiffer
from base_patch_extractor import BasePatchExtractor


class DictPatchExtractor(BasePatchExtractor):
    def __init__(self,
                 old_obj, new_obj,
                 previous_path=(), previous_new_path=(),
                 patch_extractors=[],
                 find_moved_patches=False,
                 moved_patches_similarity=0.8):

        super(DictPatchExtractor, self).__init__(old_obj, new_obj,
                                                 previous_path,
                                                 previous_new_path,
                                                 patch_extractors,
                                                 moved_patches_similarity)

        dict_diff = DictDiffer(new_obj, old_obj)

        for addition_key in dict_diff.added():
            self._add_patch('add', addition_key, new_obj[addition_key])

        for removal_key in dict_diff.removed():
            self._add_patch('remove', removal_key, old_obj[removal_key])

        for change_key in dict_diff.changed():
            if not self._try_patch_extractors(change_key, change_key):
                self._add_patch('change', change_key,
                                old_obj[change_key], new_obj[change_key])

        if find_moved_patches:
            self.patches = self._find_moved_parts()

    @classmethod
    def is_applicable(cls, old_obj, new_obj):
        return isinstance(new_obj, dict) and isinstance(old_obj, dict)

