from unittest import TestCase, main

from conflict_resolver.conflicts import get_conflicts
from utils import patches1, patches2, conflicts, assign_list_environment


class ConflictsTest(TestCase):
    def setUp(self):
        pass

    def test_get_conflicts(self):
        assign_list_environment(patches1+patches2)

        _conflicts = get_conflicts(patches1, patches2)
        self.assertEqual(conflicts, _conflicts)


if __name__ == '__main__':
    main()
