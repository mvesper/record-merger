from random import randint

from patch_extractor.list_patch_extractor import ListPatchExtractor
from patch_extractor.patch import patch


def create_random_list(max_length, max_value):
    length = randint(0, max_length-1)

    res = []
    for i in range(length):
        res.append(randint(0, max_value-1))

    return res


if __name__ == '__main__':
    for _ in range(100000):
        l1 = create_random_list(10, 10)
        l2 = create_random_list(10, 10)
        p = ListPatchExtractor(l1, l2)

        try:
            pl = patch(l1, p.patches)
            if l2 != pl:
                print l1
                print l2
                print
        except:
            print l1
            print l2
            print p.patches
            raise


'''
SOME SPECIAL CASES
old = [5]
new = [7,2,9,5,6,3,9]

old = [8]
new = [0,8,2,3]

old = [7, 6, 5, 2, 2, 7, 1]
new = [5, 0]

old = [1, 2, 4, 9, 7, 6, 6, 3]
new = [4, 3, 9]

old = [3, 5, 0, 8, 7]
new = [4, 4, 4, 5, 6]

old = [1]
new = [3, 1, 8]
'''

