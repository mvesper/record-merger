from unittest import TestCase, main

from conflict_resolver.conflicts import (_is_conflict,
                                         _get_patch_group,
                                         _is_set_environment,
                                         _pad_patch_groups,
                                         _handle_conflict,
                                         get_conflicts)
from utils import patches1, patches2, conflicts, assign_list_environment


class ConflictsTest(TestCase):
    def setUp(self):
        pass

    def test_is_conflict_regular(self):
        patch1 = {'path': ('author')}
        patch2 = {'path': ('author')}
        self.assertTrue(_is_conflict(patch1, patch2))

    def test_is_conflict_super_path(self):
        patch1 = {'path': ('author',)}
        patch2 = {'path': ('author', 1)}
        self.assertTrue(_is_conflict(patch1, patch2))

        patch1 = {'path': ('author', 1)}
        patch2 = {'path': ('author',)}
        self.assertTrue(_is_conflict(patch1, patch2))

    def test_get_patch_group(self):
        # This will not work in case that two patches are equal.
        # Therefor this needs to be avoided (using ids for example)
        patch1 = {'path': ('author', 1), 'group': 1}
        patch2 = {'path': ('author', 2), 'group': 1}
        patch3 = {'path': ('author', 3), 'group': 1}
        patch4 = {'path': ('author', 4), 'group': 1}
        patch5 = {'path': ('author', 7), 'group': 2}

        group = [patch1, patch2, patch3, patch4]
        patches = [patch1, patch2, patch3, patch4, patch5]

        index, _group = _get_patch_group(patch1, patches)
        self.assertEqual(0, index)
        self.assertEqual(group, _group)

        index, _group = _get_patch_group(patch3, patches)
        self.assertEqual(2, index)
        self.assertEqual(group, _group)

    def test_is_set_environment(self):
        self.assertTrue(_is_set_environment({'group': None}))
        self.assertTrue(_is_set_environment({'group': 1,
                                             'environment': 'set'}))
        self.assertFalse(_is_set_environment({'group': 1,
                                              'environment': 'list'}))
        self.assertFalse(_is_set_environment({'group': 1}))

    def test_pad_patch_groups(self):
        # No padding required
        patch1 = {'path': ('author', 1), 'group': 1}
        patch2 = {'path': ('author', 1), 'group': 1}
        patch1_group, patch2_group = _pad_patch_groups(patch1,
                                                       patch2,
                                                       [patch1],
                                                       [patch2])
        self.assertEqual(1, len(patch1_group))
        self.assertEqual(1, len(patch2_group))

        # Append to patch1, prepend to patch2
        patch11 = {'path': ('author', 1), 'group': 1}
        patch12 = {'path': ('author', 2), 'group': 1}
        patch21 = {'path': ('author', 2), 'group': 1}
        patch22 = {'path': ('author', 3), 'group': 1}
        patch1_group, patch2_group = _pad_patch_groups(patch12,
                                                       patch21,
                                                       [patch11, patch12],
                                                       [patch21, patch22])
        self.assertEqual(3, len(patch1_group))
        self.assertEqual(None, patch1_group[-1])
        self.assertEqual(3, len(patch2_group))
        self.assertEqual(None, patch2_group[0])

    def test_handle_conflict(self):
        # No conflict
        conflicts = []
        patch1 = {'path': 'author'}
        patch2 = {'path': 'title'}

        _handle_conflict(patch1, patch2, [patch1], [patch2], conflicts, None)

        self.assertTrue('conflicted' not in patch1)
        self.assertTrue('conflicted' not in patch2)
        self.assertEqual([], conflicts)

        # Regular conflict
        conflicts = []
        patch1 = {'path': 'author', 'group': None}
        patch2 = {'path': 'author', 'group': None}

        _handle_conflict(patch1, patch2, [patch1], [patch2], conflicts, None)

        self.assertTrue('conflicted' not in patch1)
        self.assertTrue('conflicted' not in patch2)
        self.assertEqual([([patch1], [patch2])], conflicts)

        # List conflict
        conflicts = []
        patch11 = {'path': ('author', 1), 'group': 1, 'environment': 'list'}
        patch12 = {'path': ('author', 2), 'group': 1, 'environment': 'list'}
        patch21 = {'path': ('author', 2), 'group': 1, 'environment': 'list'}
        patch22 = {'path': ('author', 3), 'group': 1, 'environment': 'list'}

        _handle_conflict(patch12, patch21,
                         [patch11, patch12], [patch21, patch22],
                         conflicts, None)

        self.assertTrue('conflicted' in patch11)
        self.assertTrue('conflicted' in patch12)
        self.assertTrue('conflicted' in patch21)
        self.assertTrue('conflicted' in patch22)
        self.assertEqual([([patch11, patch12, None],
                           [None, patch21, patch22])],
                         conflicts)

    def test_get_conflicts(self):
        assign_list_environment(patches1+patches2)

        _conflicts = get_conflicts(patches1, patches2)
        self.assertEqual(conflicts, _conflicts)


if __name__ == '__main__':
    main()
