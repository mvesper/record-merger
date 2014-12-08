from prettytable import PrettyTable


class KeyLimit(object):
    def __init__(self, key_limits=[]):
        self.final_key = '!@#$%FINAL'
        self.dict = {}
        for key_path in key_limits:
            containing = self.dict
            for key in key_path:
                try:
                    containing = containing[key]
                except KeyError:
                    containing[key] = {}
                    containing = containing[key]

            containing[self.final_key] = True

    def key_is_limit(self, key_path):
        containing = self.dict
        for key in key_path:
            try:
                containing = containing[key]
            except KeyError:
                try:
                    containing = containing['*']
                except KeyError:
                    return False

        return containing.get(self.final_key, False)


def print_patches(patches):
    fields = ['ACTION', 'PATH', 'GROUP', 'VALUE', 'MOVE']
    pt = PrettyTable(['NUMBER'] + fields)

    for i, patch in enumerate(patches):
        pt.add_row([i]+[patch.get(x.lower()) for x in fields])

    print pt


def delete_patch_at_index(index, patches, alter_group=True):
    removed_patch = patches.pop(index)

    if alter_group:
        if removed_patch['group'] is None:
            return

        if removed_patch['action'] != 'insert':
            return
        else:
            for patch in patches[index:]:
                if patch['group'] == removed_patch['group']:
                    patch['path'] = patch['path'][:-1] + (patch['path'][-1]-1,)


def delete_patch(patch, patches, alter_group=True):
    index = patches.index(patch)
    delete_patch_at_index(index, patches, alter_group)

