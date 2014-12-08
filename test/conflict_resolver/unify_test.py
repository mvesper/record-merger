from unittest import TestCase, main

from conflict_resolver.unify import (unify,
                                     _assign_id,
                                     _assign_source,
                                     _assign_conflict_index,
                                     _reassign_groups,
                                     _cleanup_patches)


up = [{'!@#$c_index':  0,
       'action': 'change',
       'group':  None,
       'path':  ('auto_resolve',),
       'take': True,
       'value': {'from': 'foo', 'to': 'bar'}},
      {'!@#$c_index':  1,
       'action': 'change',
       'group':  None,
       'path':  ('direct_rule',),
       'take': True,
       'value': {'from': 'foo', 'to': 'bar'}},
      {'!@#$c_index':  2,
       'action': 'change',
       'group':  None,
       'path':  ('indirect_rule',),
       'take': True,
       'value': {'from': 'foo', 'to': 'bar'}},
      {'!@#$c_index':  3,
       'action': 'change',
       'conflicted': True,
       'environment': 'list',
       'group':  3,
       'path':  ('list1', 0),
       'take': True,
       'value': {'from': 'foo', 'to': 'bar'}},
      {'!@#$c_index':  3,
       'action': 'change',
       'conflicted': True,
       'environment': 'list',
       'group':  3,
       'path':  ('list1', 1),
       'take': True,
       'value': {'from': 'apple', 'to': 'banana'}},
      {'!@#$c_index':  4,
       'action': 'change',
       'conflicted': True,
       'environment': 'list',
       'group':  5,
       'path':  ('list2', 0),
       'take': True,
       'value': {'from': 'foo', 'to': 'bar'}},
      {'!@#$c_index':  4,
       'action': 'change',
       'conflicted': True,
       'environment': 'list',
       'group':  5,
       'path':  ('list2', 1),
       'take': True,
       'value': {'from': 'apple', 'to': 'banana'}},
      {'!@#$c_index':  5,
       'action': 'change',
       'conflicted': True,
       'environment': 'list',
       'group':  7,
       'path':  ('list2', 3),
       'take': True,
       'value': {'from': 'strawberry', 'to': 'blueberry'}},
      {'!@#$c_index':  5,
       'action': 'change',
       'conflicted': True,
       'environment': 'list',
       'group':  7,
       'path':  ('list2', 4),
       'take': True,
       'value': {'from': 'pear', 'to': 'passion fruit'}}]


class UnifyTest(TestCase):
    def setUp(self):
        pass

    def test_assign_id(self):
        patches = [{}, {}, {}]
        _assign_id(patches)

        for i, patch in enumerate(patches):
            self.assertEqual(i, patch['!@#$id'])

    def test_assign_source(self):
        patches = [{}, {}, {}]
        _assign_source(patches, 1)

        for patch in patches:
            self.assertEqual(1, patch['!@#$source'])

    def test_assign_conflict_index(self):
        conflicts = [([{}], [{}]),
                     ([{}], [{}]),
                     ([{}], [{}])]

        _assign_conflict_index(conflicts)

        for i, (patches1, patches2) in enumerate(conflicts):
            for patch in patches1+patches2:
                self.assertEqual(i, patch['!@#$c_index'])

        # What happens if there is a None in the patches?
        conflicts = [([{}, None], [{}, None]),
                     ([{}], [{}]),
                     ([{}], [{}])]

        _assign_conflict_index(conflicts)

        for i, (patches1, patches2) in enumerate(conflicts):
            for patch in patches1+patches2:
                if patch is None:
                    continue
                self.assertEqual(i, patch['!@#$c_index'])

    def test_reassign_groups(self):
        # Reassignment of non conflicting patches
        patches1 = [{'path': ('author', 0), 'group': 1},
                    {'path': ('author', 1), 'group': 1},
                    {'path': ('author', 2), 'group': 1}]
        patches2 = [{'path': ('author', 7), 'group': 2},
                    {'path': ('author', 8), 'group': 2},
                    {'path': ('author', 9), 'group': 2}]

        _assign_source(patches1, 1)
        _assign_source(patches2, 2)

        _reassign_groups(patches1+patches2)

        for patch in patches1:
            self.assertEqual(0, patch['group'])
        for patch in patches2:
            self.assertEqual(3, patch['group'])

        # Conflicting
        patches1 = [{'path': ('author', 0), 'group': 1, '!@#$c_index': 1},
                    {'path': ('author', 1), 'group': 1, '!@#$c_index': 1},
                    {'path': ('author', 2), 'group': 1, '!@#$c_index': 1}]
        patches2 = [{'path': ('author', 2), 'group': 2, '!@#$c_index': 1},
                    {'path': ('author', 3), 'group': 2, '!@#$c_index': 1},
                    {'path': ('author', 4), 'group': 2, '!@#$c_index': 1}]

        _assign_source(patches1, 1)
        _assign_source(patches2, 2)

        _reassign_groups(patches1+patches2)

        for patch in patches1+patches2:
            self.assertEqual(0, patch['group'])

        # Conflicting and non-conflicting
        patches1 = [{'path': ('author', 0), 'group': 1, '!@#$c_index': 1},
                    {'path': ('author', 1), 'group': 1, '!@#$c_index': 1},
                    {'path': ('author', 2), 'group': 1, '!@#$c_index': 1},
                    {'path': ('author', 10), 'group': 2},
                    {'path': ('author', 11), 'group': 2}]
        patches2 = [{'path': ('author', 2), 'group': 2, '!@#$c_index': 1},
                    {'path': ('author', 3), 'group': 2, '!@#$c_index': 1},
                    {'path': ('author', 4), 'group': 2, '!@#$c_index': 1},
                    {'path': ('author', 12), 'group': 3},
                    {'path': ('author', 14), 'group': 4}]

        _assign_source(patches1, 1)
        _assign_source(patches2, 2)

        _reassign_groups(patches1+patches2)

        for patch in patches1[:3]+patches2[:3]:
            self.assertEqual(0, patch['group'])

        for patch in patches1[3:]:
            self.assertEqual(3, patch['group'])

        self.assertEqual(8, patches2[3]['group'])
        self.assertEqual(9, patches2[4]['group'])

    def test_cleanup_patches(self):
        patches = [{'!@#$id': 1},
                   {'!@#$c_index':  2},
                   {'!@#$source': 3}]

        _cleanup_patches(patches)

        self.assertEqual([{}, {}, {}], patches)

    def test_unify(self):
        patches1 = [{'path': ('author', 0), 'group': 1, 'take': True},
                    {'path': ('author', 1), 'group': 1, 'take': True},
                    {'path': ('author', 2), 'group': 1, 'take': False},
                    {'path': ('author', 10), 'group': 2, 'take': True},
                    {'path': ('author', 11), 'group': 2, 'take': True}]
        patches2 = [{'path': ('author', 2), 'group': 2, 'take': True},
                    {'path': ('author', 3), 'group': 2, 'take': True},
                    {'path': ('author', 4), 'group': 2, 'take': True},
                    {'path': ('author', 12), 'group': 3, 'take': True},
                    {'path': ('author', 14), 'group': 4, 'take': True}]

        conflicts = [([patches1[0], patches1[1], patches1[2], None, None],
                      [None, None, patches2[0], patches2[1], patches2[2]])]

        up = unify(patches1, patches2, conflicts)

        self.assertEqual(9, len(up))

        for patch in patches1+patches2:
            self.assertEqual(3, len(patch.keys()))

        for patch in up[:2]:
            self.assertEqual(1, patch['!@#$source'])
            self.assertEqual(0, patch['group'])

        self.assertEqual(2, up[2]['!@#$source'])
        self.assertEqual(0, up[2]['group'])

        for patch in up[3:5]:
            self.assertEqual(2, patch['!@#$source'])
            self.assertEqual(0, patch['group'])

        for patch in up[5:7]:
            self.assertEqual(1, patch['!@#$source'])
            self.assertEqual(2, patch['group'])

        self.assertEqual(2, up[7]['!@#$source'])
        self.assertEqual(7, up[7]['group'])

        self.assertEqual(2, up[8]['!@#$source'])
        self.assertEqual(8, up[8]['group'])

        self.assertEqual(up, sorted(up, key=lambda x: (x['group'], x['path'][-1])))

if __name__ == '__main__':
    main()

'''
from copy import deepcopy
from conflict_resolver.unify import unify
from conflict_resolver.resolver import resolve
from conflict_resolver.conflicts import get_conflicts, print_conflicts
from config_manager.manager import ConfigManager
from test.conflict_resolver.utils import patches1, patches2, assign_list_environment

assign_list_environment(patches1+patches2)

p1 = deepcopy(patches1)
p2 = deepcopy(patches2)
c = get_conflicts(p1, p2)

conflicts = get_conflicts(patches1, patches2)

config_manager = ConfigManager('test/conflict_resolver/test_conf_action.conf')

resolution = resolve(patches1, patches2, conflicts,
                     config_manager.get_conflict_actions())

resolve(p1, p2, c, config_manager.get_conflict_actions())

up = [x for x in p1+p2 if 'take' not in x or ('take' in x and x['take'])]
'''
