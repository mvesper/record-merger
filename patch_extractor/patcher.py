from copy import deepcopy


def patchit(old_obj, patches):
    working_obj = deepcopy(old_obj)

    for patch in patches:
        patch.action(working_obj, patch.path, patch.value)

    return working_obj

