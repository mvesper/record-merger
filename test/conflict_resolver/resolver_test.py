from unittest import TestCase, main

from conflict_resolver.resolver import (resolve,
                                        _find_conflicting_path,
                                        _auto_resolve)


class ResolverTest(TestCase):
    def setUp(self):
        pass

    def test_find_conflicting_path(self):
        # Regular
        patch1 = {'path': ('foo', 'bar', 'banana')}
        patch2 = {'path': ('foo', 'bar')}
        path = _find_conflicting_path([patch1], [patch2])

        self.assertEqual(patch2['path'], path)

        patch1 = {'path': ('foo', 'bar')}
        patch2 = {'path': ('foo', 'bar')}
        path = _find_conflicting_path([patch1], [patch2])

        self.assertEqual(patch2['path'], path)

        # Patches filled with Nones
        patch1 = {'path': ('foo', 'bar')}
        patch2 = {'path': ('foo', 'bar', 'apple')}
        path = _find_conflicting_path([None, None, None, patch1],
                                      [None, None, patch2])

        self.assertEqual(patch1['path'], path)

    def test_auto_resolve(self):
        # Single patch success
        patch1 = {'path': ('author', 1), 'action': 'insert', 'value': 1}
        patch2 = {'path': ('author', 1), 'action': 'insert', 'value': 1}
        result = _auto_resolve([patch1], [patch2])

        self.assertTrue(result)
        self.assertTrue(patch1['take'])
        self.assertFalse(patch2['take'])

        # Multiple patches success
        patch11 = {'path': ('author', 1), 'action': 'insert', 'value': 1}
        patch12 = {'path': ('author', 1), 'action': 'insert', 'value': 1}
        patch21 = {'path': ('author', 1), 'action': 'insert', 'value': 1}
        patch22 = {'path': ('author', 1), 'action': 'insert', 'value': 1}
        result = _auto_resolve([patch11, patch12], [patch21, patch22])

        self.assertTrue(result)
        self.assertTrue(patch12['take'])
        self.assertTrue(patch12['take'])
        self.assertFalse(patch21['take'])
        self.assertFalse(patch22['take'])

        # Fail
        patch1 = {'path': ('author', 1), 'action': 'insert', 'value': 1}
        patch2 = {'path': ('author', 1), 'action': 'insert', 'value': 2}
        result = _auto_resolve([patch1], [patch2])

        self.assertFalse(result)

        # Fail due to None in list
        patch1 = {'path': ('author', 1), 'action': 'insert', 'value': 1}
        patch2 = {'path': ('author', 1), 'action': 'insert', 'value': 1}
        result = _auto_resolve([patch1, None], [None, patch2])

        self.assertFalse(result)

    def test_resolve(self):
        # Since auto resolve is already tested, just test unresolved
        patch1 = {'path': ('author', 1), 'action': 'insert', 'value': 1}
        patch2 = {'path': ('author', 1), 'action': 'insert', 'value': 2}
        conflicts = [([patch1], [patch2])]
        actions = {}

        unresolved_conflicts = resolve([patch1], [patch2], conflicts, actions)

        self.assertEqual(unresolved_conflicts, conflicts)


if __name__ == '__main__':
    main()
