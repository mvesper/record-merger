from unittest import TestCase, main

from conflict_resolver.resolver import resolve
from conflict_resolver.conflicts import get_conflicts
from config_manager.manager import ConfigManager
from utils import patches1, patches2, assign_list_environment


class ResolverTest(TestCase):
    def setUp(self):
        pass

    def test_get_conflicts(self):
        assign_list_environment(patches1+patches2)
        conflicts = get_conflicts(patches1, patches2)

        config_manager = ConfigManager('test/conflict_resolver/test_conf_action.conf')

        resolution = resolve(patches1, patches2, conflicts,
                             config_manager.get_conflict_actions())

        self.assertEqual(resolution, [])


if __name__ == '__main__':
    main()
