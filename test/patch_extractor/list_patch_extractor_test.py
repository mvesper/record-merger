from unittest import TestCase, main
from itertools import product

from patch_extractor.list_patch_extractor import ListPatchExtractor


class TestListPatchExtractor(TestCase):
    def setUp(self):
        pass

    def test_extraction_basic(self):
        old1 = []
        new1 = [1]
        patch1 =  {'action': 'add',
                   'group': 0,
                   'path': (0,),
                   'value': {'from': None, 'to': 1}}
        
        lpe = ListPatchExtractor(old1, new1)
        self.assertEqual(lpe.patches[0], patch1)


        old2 = [1]
        new2 = []
        patch2 =  {'action': 'remove',
                   'group': 0,
                   'path': (0,),
                   'value': {'from': 1, 'to': None}}
        
        lpe = ListPatchExtractor(old2, new2)
        self.assertEqual(lpe.patches[0], patch2)


        old3 = [1]
        new3 = [2]
        patch3 =  {'action': 'change',
                   'group': 0,
                   'path': (0,),
                   'value': {'from': 1, 'to': 2}}
        
        lpe = ListPatchExtractor(old3, new3)
        self.assertEqual(lpe.patches[0], patch3)


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

        applicables = [_list]
        not_applicables = [_dict, _set, _tuple, _string, _obj, _int, _float]

        self.assertTrue(ListPatchExtractor.is_applicable(_list, _list))

        true_false = map(lambda x: ListPatchExtractor.is_applicable(*x), product(applicables, not_applicables))
        self.assertFalse(any(true_false))

        false_false = map(lambda x: ListPatchExtractor.is_applicable(*x), product(not_applicables, not_applicables))
        self.assertFalse(any(false_false))


if __name__ == '__main__':
    main()
