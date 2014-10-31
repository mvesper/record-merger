import types as t

from dict_patch_extractor import DictPatchExtractor
from utils import KeyLimit


class ObjectPatchExtractor(DictPatchExtractor):
    def __init__(self,
                 old_obj, new_obj,
                 previous_path=(), previous_new_path=(),
                 patch_extractors=[],
                 key_limits=KeyLimit(),
                 find_moved_patches=False,
                 moved_patches_similarity=0.8):

        old_obj = old_obj.__dict__
        new_obj = new_obj.__dict__

        super(ObjectPatchExtractor, self).__init__(old_obj, new_obj,
                                                   previous_path,
                                                   previous_new_path,
                                                   patch_extractors,
                                                   key_limits,
                                                   find_moved_patches,
                                                   moved_patches_similarity)

    @classmethod
    def is_applicable(cls, old_obj, new_obj):
        types = t.__getattribute__('__builtins__').values() 
        return (isinstance(new_obj, object) and
                isinstance(old_obj, object) and
                type(new_obj) not in types and
                type(old_obj) not in types)

