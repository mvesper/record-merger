from unittest import TestCase, main

from conflict_resolver.unify import unify
from conflict_resolver.resolver import resolve
from conflict_resolver.conflicts import get_conflicts
from config_manager.manager import ConfigManager
from utils import patches1, patches2, assign_list_environment


up = [{'!@#$c_index': 0,
       'action': 'change',
       'group': None,
       'path': ('auto_resolve',),
       'take': True,
       'value': {'from': 'foo', 'to': 'bar'}},
      {'!@#$c_index': 1,
       'action': 'change',
       'group': None,
       'path': ('direct_rule',),
       'take': True,
       'value': {'from': 'foo', 'to': 'bar'}},
      {'!@#$c_index': 2,
       'action': 'change',
       'group': None,
       'path': ('indirect_rule',),
       'take': True,
       'value': {'from': 'foo', 'to': 'bar'}},
      {'!@#$c_index': 3,
       'action': 'change',
       'conflicted': True,
       'environment': 'list',
       'group': 3,
       'path': ('list1', 0),
       'take': True,
       'value': {'from': 'foo', 'to': 'bar'}},
      {'!@#$c_index': 3,
       'action': 'change',
       'conflicted': True,
       'environment': 'list',
       'group': 3,
       'path': ('list1', 1),
       'take': True,
       'value': {'from': 'apple', 'to': 'banana'}},
      {'!@#$c_index': 4,
       'action': 'change',
       'conflicted': True,
       'environment': 'list',
       'group': 5,
       'path': ('list2', 0),
       'take': True,
       'value': {'from': 'foo', 'to': 'bar'}},
      {'!@#$c_index': 4,
       'action': 'change',
       'conflicted': True,
       'environment': 'list',
       'group': 5,
       'path': ('list2', 1),
       'take': True,
       'value': {'from': 'apple', 'to': 'banana'}},
      {'!@#$c_index': 5,
       'action': 'change',
       'conflicted': True,
       'environment': 'list',
       'group': 7,
       'path': ('list2', 3),
       'take': True,
       'value': {'from': 'strawberry', 'to': 'blueberry'}},
      {'!@#$c_index': 5,
       'action': 'change',
       'conflicted': True,
       'environment': 'list',
       'group': 7,
       'path': ('list2', 4),
       'take': True,
       'value': {'from': 'pear', 'to': 'passion fruit'}}]


class UnifyTest(TestCase):
    def setUp(self):
        pass

    def test_get_conflicts(self):
        assign_list_environment(patches1+patches2)
        conflicts = get_conflicts(patches1, patches2)

        config_manager = ConfigManager('test/conflict_resolver/test_conf_action.conf')

        resolution = resolve(patches1, patches2, conflicts,
                             config_manager.get_conflict_actions())

        unified_patches = unify(patches1, patches2, conflicts)

        self.assertEqual(unified_patches, up)


if __name__ == '__main__':
    main()

'''
from copy import deepcopy
from conflict_resolver.unify import unify, _change_conflicting_groups, _reassign_groups
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
