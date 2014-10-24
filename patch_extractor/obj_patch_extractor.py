from types import InstanceType

from dict_patch_extractor import DictPatchExtractor


class ObjectPatchExtractor(DictPatchExtractor):
    def __init__(self,
                 old_obj, new_obj,
                 previous_path=(), previous_new_path=(),
                 patch_extractors=[],
                 find_moved_patches=False,
                 moved_patches_similarity=0.8):

        old_obj = old_obj.__dict__
        new_obj = new_obj.__dict__

        super(ObjectPatchExtractor, self).__init__(old_obj, new_obj,
                                                   previous_path,
                                                   previous_new_path,
                                                   patch_extractors,
                                                   find_moved_patches,
                                                   moved_patches_similarity)

    @classmethod
    def is_applicable(cls, old_obj, new_obj):
        return (isinstance(new_obj, object) and
                isinstance(old_obj, object) and
                type(new_obj) is InstanceType and
                type(old_obj) is InstanceType)

