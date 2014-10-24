from patch_extractor.diff import diff
from patch_extractor.base_patch_extractor import BasePatchExtractor

old = {'a': 'Hello'}
new = {'b': 'Hello'}

p = diff(old, new)

bpe = BasePatchExtractor(old, new)
bpe.patches = p

bpe._find_moved_parts()


old = {'a': 'Hello', 'b': 'utz'}
new = {'a': 'utz'}

old = {'a': 'Hello', 'b': 'utz'}
new = {'a': 'utz', 'b': 'Hello'}

old = {'a': {1:1, 2:2}}
new = {'b': {1:1, 2:2}}

# BULLSHIT
def bla(patches, patch1, patch2, i, j, comp_val1, comp_val2, action1, action2):
    if patch1[0] == action1 and patch2[0] == action2:
        _similarity = self._estimate_similarity(com_val1, comp_val2)
        if _similarity > similarity:
            patches[j] = ('move',
                          patch2[1],
                          patch2[2],
                          patch2[3],
                          (patch1[1], 'add', 'remove'))
            patches[i] = ('cleared',)
    return False


def _create_move_patch(self, patches, patch1, patch2, i, j,
                       comp_val1, comp_val2, action1, action2):
    _similarity = self._estimate_similarity(comp_val1, comp_val2)
    if _similarity > similarity:
        patches[i] = ('move',
                      patch1[1],
                      patch1[2],
                      patch1[3],
                      (patch2[1], action1, action2))
        patches[j] = ('cleared',)


if patch1[0] == 'add' and patch2[0] == 'remove':
    self.create_move_patch(patches, patch1, patch2, i, j, patch1[2], patch2[2], 'add', 'remove')

if patch1[0] == 'remove' and patch2[0] == 'add':
    self.create_move_patch(patches, patch2, patch1, j, i, patch2[2], patch1[2], 'add', 'remove')

if patch1[0] == 'change' and patch2[0] == 'remove':
    self.create_move_patch(patches, patch1, patch2, i, j, patch1[2][1], patch2[2], 'change', 'remove')

if patch1[0] == 'remove' and patch2[0] == 'change':
    self.create_move_patch(patches, patch2, patch1, j, i, patch2[2][1], patch1[2], 'change', 'remove')
