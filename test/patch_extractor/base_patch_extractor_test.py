from unittest import TestCase, main
from itertools import product
from difflib import SequenceMatcher

from patch_extractor.base_patch_extractor import BasePatchExtractor
from patch_extractor.list_patch_extractor import ListPatchExtractor
from patch_extractor.dict_patch_extractor import DictPatchExtractor
from patch_extractor.obj_patch_extractor import ObjectPatchExtractor
from patch_extractor.utils import KeyLimit


class ObjectDictPatchExtractor(TestCase):
    def setUp(self):
        self.bpe = BasePatchExtractor(None, None)
        pass

    def test_add_patch(self):
        self.assertEqual(self.bpe.patches, [])
        self.bpe._add_patch('add', 'path', None, 'Hello', 1)
        self.assertEqual(self.bpe.patches, [{'action': 'add', 'path': ('path',), 'value': {'from': None, 'to': 'Hello'}, 'group': 1}])
        self.bpe.patches = []

    def test_create_patch(self):
        cp = self.bpe._create_patch('add', 'path', None, 'Hello', 1)
        self.assertEqual(cp, {'action': 'add', 'path': ('path',), 'value': {'from': None, 'to': 'Hello'}, 'group': 1})

    def test_try_patch_extractors(self):
        # is_applicable method and general functionality is tested in the specific files 
        self.bpe.old_obj = {'foo': ['bar']}
        self.bpe.new_obj = {'foo': ['bar']}

        #TEST KEY LIMIT
        self.bpe.key_limits = KeyLimit([('foo',)])
        self.assertFalse(self.bpe._try_patch_extractors('foo', 'foo'))
        self.bpe.key_limits = KeyLimit()

        #TEST NO patch extractors
        self.assertFalse(self.bpe._try_patch_extractors('foo', 'foo'))

        #TEST patch extractors
        self.bpe.patch_extractors = [ListPatchExtractor, DictPatchExtractor, ObjectPatchExtractor]
        self.assertTrue(self.bpe._try_patch_extractors('foo', 'foo'))

    def test_try_patch_extractors_for_ungrouping(self):
        # is_applicable method and general functionality is tested in the specific files 
        self.bpe.old_obj = {'foo': ['bar']}
        self.bpe.new_obj = {'foo': ['bar']}

        #TEST KEY LIMIT
        self.bpe.key_limits = KeyLimit([('foo',)])
        self.assertFalse(self.bpe._try_patch_extractors_for_ungrouping('foo'))
        self.bpe.key_limits = KeyLimit()

        #TEST NO patch extractors
        self.assertFalse(self.bpe._try_patch_extractors_for_ungrouping('foo'))

        #TEST patch extractors
        self.bpe.patch_extractors = [ListPatchExtractor, DictPatchExtractor, ObjectPatchExtractor]
        self.assertTrue(self.bpe._try_patch_extractors_for_ungrouping('foo'))

    def test_stringigy(self):
        d = {'a': 'a', 'b': 'b', 'c': 'c'}
        self.assertEqual(self.bpe._stringify(d), '{"a": "a", "b": "b", "c": "c"}')

    def test_estimate_similarity(self):
        s = 'Hello, World!'
        sequence = SequenceMatcher(None, s, s)
        self.assertEqual(self.bpe._estimate_similarity(s, s), sequence.ratio())

    def test_create_move_patch(self):
        patch1 = {'action': 'add',
                  'path': ('path_new',),
                  'value': {'from': None, 'to': 'Hello'},
                  'group': None}
        patch2 = {'action': 'remove',
                  'path': ('path_old',),
                  'value': {'from': 'Hello', 'to': None},
                  'group': None}
        moved = {'action': 'move',
                 'path': ('path_new',),
                 'value': {'from': None, 'to': 'Hello'},
                 'group': None,
                 'move': {'moved_from': patch2['path'], 'old_action': 'add', 'new_action': 'remove'}}

        self.bpe._create_move_patch(patch1, patch2, patch1['value']['to'], patch2['value']['from'], 'add', 'remove')
        self.assertEqual(patch1, moved)

    def test_find_moved_parts(self):
        old1 = {'a': 'Hello'}
        new1 = {'b': 'Hello'}
        moved1 = {'action': 'move',
                  'path': ('b',),
                  'value': {'from': None, 'to': 'Hello'},
                  'group': None,
                  'move': {'moved_from': ('a',), 'old_action': 'add', 'new_action': 'remove'}}

        dpe = DictPatchExtractor(old1, new1, find_moved_patches=True)
        self.assertEqual(dpe.patches[0], moved1)

        old2 = {'a': 'Hello', 'b': 'utz'}
        new2 = {'a': 'utz'}
        moved2 = {'action': 'move',
                  'path': ('a',),
                  'value': {'from': 'Hello', 'to': 'utz'},
                  'group': None,
                  'move': {'moved_from': ('b',), 'old_action': 'change', 'new_action': 'remove'}}

        dpe = DictPatchExtractor(old2, new2, find_moved_patches=True)
        self.assertEqual(dpe.patches[0], moved2)

        old3 = {'a': 'Hello', 'b': 'utz'}
        new3 = {'a': 'utz', 'b': 'Hello'}
        moved3 = [{'action': 'move',
                   'group': None,
                   'move': {'moved_from': ('b',),
                            'new_action': 'dont_remove',
                            'old_action': 'change'},
                   'path': ('a',),
                   'value': {'from': 'Hello', 'to': 'utz'}},
                  {'action': 'move',
                   'group': None,
                   'move': {'moved_from': ('a',),
                            'new_action': 'dont_remove',
                            'old_action': 'change'},
                   'path': ('b',),
                   'value': {'from': 'utz', 'to': 'Hello'}}]

        dpe = DictPatchExtractor(old3, new3, find_moved_patches=True)
        self.assertEqual(dpe.patches, moved3)


if __name__ == '__main__':
    main()
