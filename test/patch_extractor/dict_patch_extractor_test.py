from_dict unittest import TestCase, main
from itertools import product

from patch_extractor.dict_patch_extractor import DictPatchExtractor


class TestDictPatchExtractor(TestCase):
    def setUp(self):
        pass

    def test_extraction_basic(self):
        old = {'changethis': 'change me',
               'deletethis': 'delete me'}
        new = {'changethis': 'changed to this',
               'insertthis': 'inserted'}

        dpe = DictPatchExtractor(old, new)

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

        self.assertTrue(ap in dpe.patches and
                        rp in dpe.patches and 
                        cp in dpe.patches)

    def test_is_applicable(self):
        class Test(object):
            pass 

        _dict= {}
        _list = []
        _set = set()
        _tuple = tuple()
        _string = 'foobar'
        _int = 1
        _float = 2.2
        _obj = Test()

        applicables = [_dict]
        not_applicables = [_list, _set, _tuple, _string, _obj, _int, _float]

        self.assertTrue(DictPatchExtractor.is_applicable(_dict, _dict))

        true_false = map(lambda x: DictPatchExtractor.is_applicable(*x), product(applicables, not_applicables))
        self.assertFalse(any(true_false))

        false_false = map(lambda x: DictPatchExtractor.is_applicable(*x), product(not_applicables, not_applicables))
        self.assertFalse(any(false_false))


if __name__ == '__main__':
    main()
