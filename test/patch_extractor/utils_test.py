from unittest import TestCase, main
from patch_extractor.utils import (KeyLimit,
                                   delete_patch)


class UtilsTest(TestCase):
    def setUp(self):
        pass

    def test_delete_patch(self):
        # None group
        patches = [{'group': None, 'id': 0},
                   {'group': None, 'id': 1},
                   {'group': None, 'id': 2}]

        delete_patch(patches[0], patches)

        self.assertEqual(1, patches[0]['id'])
        self.assertEqual(2, patches[1]['id'])

        delete_patch(patches[1], patches)

        self.assertEqual(1, patches[0]['id'])

        delete_patch(patches[0], patches)

        self.assertEqual(0, len(patches))

        # non None group, no insert action
        patches = [{'group': 1, 'action': 'change', 'id': 0},
                   {'group': 1, 'action': 'change', 'id': 1},
                   {'group': 1, 'action': 'change', 'id': 2}]

        delete_patch(patches[0], patches)

        self.assertEqual(1, patches[0]['id'])
        self.assertEqual(2, patches[1]['id'])

        delete_patch(patches[1], patches)

        self.assertEqual(1, patches[0]['id'])

        delete_patch(patches[0], patches)

        self.assertEqual(0, len(patches))

        # non None group, insert action
        patches = [{'group': 1, 'action': 'insert', 'path': (0,), 'id': 0},
                   {'group': 1, 'action': 'insert', 'path': (1,), 'id': 1},
                   {'group': 1, 'action': 'insert', 'path': (2,), 'id': 2}]

        delete_patch(patches[1], patches)

        self.assertEqual((0,), patches[0]['path'])
        self.assertEqual((1,), patches[1]['path'])

        delete_patch(patches[0], patches)

        self.assertEqual((0,), patches[0]['path'])

        # non None group, inser action, alter_group=False
        patches = [{'group': 1, 'action': 'insert', 'path': (0,), 'id': 0},
                   {'group': 1, 'action': 'insert', 'path': (1,), 'id': 1},
                   {'group': 1, 'action': 'insert', 'path': (2,), 'id': 2}]

        delete_patch(patches[0], patches, alter_group=False)

        self.assertEqual((1,), patches[0]['path'])
        self.assertEqual((2,), patches[1]['path'])

        delete_patch(patches[0], patches, alter_group=False)

        self.assertEqual((2,), patches[0]['path'])

    def test_keylimit(self):
        limits = [('author', '*'), ('foo', 'bar')]
        key_limit = KeyLimit(limits)

        self.assertTrue(key_limit.key_is_limit(('author', 1)))
        self.assertTrue(key_limit.key_is_limit(('author', 2)))
        self.assertTrue(key_limit.key_is_limit(('author', 3)))

        self.assertFalse(key_limit.key_is_limit(('author',)))
        self.assertFalse(key_limit.key_is_limit(('author', 'foo', 1)))
        self.assertFalse(key_limit.key_is_limit(('author', 'foo', 2)))
        self.assertFalse(key_limit.key_is_limit(('author', 'foo', 3)))

        self.assertTrue(key_limit.key_is_limit(('foo', 'bar')))
        self.assertFalse(key_limit.key_is_limit(('foo',)))
        self.assertFalse(key_limit.key_is_limit(('foo', 'bar', 'banana')))

        self.assertFalse(key_limit.key_is_limit(('utz',)))
        self.assertFalse(key_limit.key_is_limit(('utz', 'utz', 'utz')))


if __name__ == '__main__':
    main()
