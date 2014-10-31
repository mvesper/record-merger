from unittest import TestCase, main
from itertools import product

from patch_extractor.obj_patch_extractor import ObjectPatchExtractor


class Test(object):
    pass 


class ObjectDictPatchExtractor(TestCase):
    def setUp(self):
        pass

    def test_extraction_basic(self):
        old = Test()
        old.changethis = 'change me'
        old.deletethis = 'delete me'
        new = Test()
        new.changethis = 'changed to this'
        new.insertthis = 'inserted'

        ope = ObjectPatchExtractor(old, new)

        ap = {'action': 'add',
              'group': None,
              'path': ('insertthis',),
              'value': {'from': None, 'to': 'inserted'}}
        rp = {'action': 'remove',
              'group': None,
              'path': ('deletethis',),
              'value': {'from': 'delete me', 'to': None}}
        cp = {'action': 'change',
              'group': None,
              'path': ('changethis',),
              'value': {'from': 'change me', 'to': 'changed to this'}}

        self.assertTrue(ap in ope.patches and
                        rp in ope.patches and 
                        cp in ope.patches)

    def test_is_applicable(self):
        _dict= {}
        _list = []
        _set = set()
        _tuple = tuple()
        _string = 'foobar'
        _int = 1
        _float = 2.2
        _obj = Test()

        applicables = [_obj]
        not_applicables = [_list, _set, _tuple, _string, _dict, _int, _float]

        self.assertTrue(ObjectPatchExtractor.is_applicable(_obj, _obj))

        true_false = map(lambda x: ObjectPatchExtractor.is_applicable(*x), product(applicables, not_applicables))
        self.assertFalse(any(true_false))

        false_false = map(lambda x: ObjectPatchExtractor.is_applicable(*x), product(not_applicables, not_applicables))
        self.assertFalse(any(false_false))


if __name__ == '__main__':
    main()
