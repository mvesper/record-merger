from obj_patch_extractor import ObjectPatchExtractor
from dict_patch_extractor import DictPatchExtractor
from list_patch_extractor import ListPatchExtractor


def diff(old, new,
         extend_extractors=[],
         ignore_extractors=[]):
    extractors = [DictPatchExtractor, ListPatchExtractor, ObjectPatchExtractor]

    extractors.extend(extend_extractors)

    for extractor in ignore_extractors:
        extractors.remove(extractor)

    for extractor in extractors:
        if extractor.is_applicable(old, new):
            e = extractor(old, new, patch_extractors=extractors)
            return e.patches

    return []
