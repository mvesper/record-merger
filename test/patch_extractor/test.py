from pprint import pprint

from patch_extractor.diff import diff
from patch_extractor.patch import patch 

class Test():
    pass

a = Test()
a.change = 'foo'
a.remove = 'del'

b = Test()
b.change = 'bar'
b.add = 'wuhu'


old = {'a': 'This is a string that is going to change',
       'b': [1, 2, 3],      # Let's insert something here
       'c': [1, 2, 3],      # Let's delete something here
       'd': ['aa', 'ab'],   # Let's change something here
       'e': 1.1,            # Numbers should be easy            
       'f': 'remove me',    # This is going to be removed
       'changethis': {'a':1, 'b':[1,2]},
       'listtest':[1, 2, 3, 4],
       'nested':[{'a': 1}, {'b':1}],
       'object':a
       }
new = {'a': 'And now this string changed',
       'b': [1, 2, 3, 4],   # Let's insert something here
       'c': [1, 2],         # Let's delete something here
       'd': ['aa', 'abc'],  # Let's change something here
       'e': 2.2,            # Numbers should be easy     
       'g': 'added',        # added
       'insertthis': {'a':1, 'b': [1,2]},
       'changethis': {'a':2, 'b': [1]},
       'listtest':[-1, 0, 1, 2, 4, 5, 6],
       'nested':[{'a': 1}, {'b':2}],
       'object':b
       }

patches = diff(old, new)

pprint(patches)
print

patched_obj = patch(old, patches)
pprint(patched_obj)

'''
from patch_extractor.dict_patch_extractor import DictPatchExtractor
from patch_extractor.list_patch_extractor import ListPatchExtractor
#from patch_extractor.actions import insert_action, delete_action
from patch_extractor.patcher import Patcher
from patch_filter import _resolve_list_problems

old = {'a': [1,2,3,4,5,6]}
new1 = {'a': [3,4,5,6]}
new2 = {'a': [1,2,5,6]}

e = DictPatchExtractor(old, new1, patch_extractors=[DictPatchExtractor, ListPatchExtractor])
e1 = DictPatchExtractor(old, new2, patch_extractors=[DictPatchExtractor, ListPatchExtractor])


from patch_extractor.list_patch_extractor import ListPatchExtractor
#from patch_extractor.actions import insert_action, delete_action
from patch_extractor.patcher import Patcher
from patch_filter import _resolve_list_problems

old = [1,2,3,4,5,6]
new1 = [3,4,5,6]
new2 = [1,2,5,6]

e = ListPatchExtractor(old, new1, patch_extractors=[ListPatchExtractor])
e1 = ListPatchExtractor(old, new2, patch_extractors=[ListPatchExtractor])

for p in e.patches:
    merge_list_patch(p, e.patches, e1.patches, None, None, None, [])
'''


old = [1,2,3,4,5]
new = [2,3,6,7,4,8,9]


old = {'a':{'c':1}, 'b':2}
new = {'d':{'c':1}, 'b':2}
