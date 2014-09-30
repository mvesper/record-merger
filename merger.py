from patch_extractor.dict_patch_extractor import DictPatchExtractor
from patch_extractor.list_patch_extractor import ListPatchExtractor

from patch_extractor.patcher import patchit
from patch_filter import filter_patches, filter_patches_for_comparsion, merge_patches


# There needs to be a better naming going on.
# Calling everythin record might be misleading
def merge(record1, record2):
    # Step 1: Find the 'latest common ancestor'.
    #         If this fails:
    #         Get earliest versions of records.
    i, j, lca = find_latest_ancestor(record1, record2)
    # Step 2: In case LCA is not found:
    #         Somehow 'merge' those two records
    if not lca:
        lca = create_virtual_lca(record1.internal_records[i],
                                 record2.internal_records[j])
    # Setp 3: get patches starting from lca
        # TODO
        # Do we need to get a series of patches? Maybe lca -> current is enough...
    record1_patches = get_patches(record1.internal_records[0], lca)
    record2_patches = get_patches(record2.internal_records[0], lca)
    # Step 4: filter patches
    record1_patches = filter_patches(record1,
                                     record1_patches,
                                     record1.source, record2.source,
                                     record1.source)
    record2_patches = filter_patches(record2,
                                     record2_patches,
                                     record1.source, record2.source,
                                     record2.source)
    # Step 5: Find potential merge conflicts
        # TODO
        # patches = resolve_confilcts(record1_patches, record2_patches,
        #                             record1.source, record2.source)
    try:
        patches = merge_patches(record1_patches, record2_patches,
                                record1.source, record2.source,
                                record1.internal_records[0],
                                record2.internal_records[0])
    except:
        # TODO
        raise
    # Step 6: Apply patches to merged record
    return patchit(lca, patches)


def find_latest_ancestor(record1, record2):
    for i, _record1 in enumerate(record1.internal_records):
        for j, _record2 in enumerate(record2.internal_records):
            extractors = [DictPatchExtractor, ListPatchExtractor]
            extractor = DictPatchExtractor(_record1, _record2,
                                           patch_extractors=extractors)
            if not filter_patches_for_comparsion(_record1,
                                                 extractor.patches,
                                                 record1.source,
                                                 record2.source):
                return i, j, _record1
    else:
        return i, j, None


def create_virtual_lca(record1, record2):
    # TODO: There should be multiple ways to create a useful lca
    #   * an empty dict is just the simplest way to do it
    return {}


def get_patches(latest_record, lca):
    # TODO: Do we need to get the patches from all the consecutive updates?
    # Maybe it is enough to just go from lca to current...
    #   * Probably not specific enough
    #   * Example: 2 patches inserting a dict, but the dict looks completly different
    #   * SOLUTION
    #       * It should be specific enough and actually solves a lot of problems
    extractors = [DictPatchExtractor, ListPatchExtractor]
    extractor = DictPatchExtractor(lca, latest_record,
                                   patch_extractors=extractors)
    return extractor.patches

