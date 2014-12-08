from dictdiffer import diff, EXTRACTORS, SequenceExtractor
from patch_converter.wrapper import wrap, SequenceWrapper
from conflict_resolver.conflicts import get_conflicts, print_conflicts
from conflict_resolver.resolver import resolve
from conflict_resolver.unify import unify
from utils import WildcardDict

old = {'foo': 'bar',
       'insert_list': [3],
       'change_list': [0,1,2,3,4,5,6]}

new1 = {'foo': 'foo-bar',
        'insert_list': [1,2,3,4,5],
        'change_list': [0,-1,-2,-3,-4,-5,6]}

new2 = {'foo': 'bar-foo',
        'insert_list': [1,2,3],
        'change_list': [0,-1,2,3,4,-5,6]}

e = EXTRACTORS
e[('insert_list',)] = [SequenceExtractor]
e[('change_list',)] = [SequenceExtractor]

diff1 = list(diff(old, new1, expand=True, extractors=e))
diff2 = list(diff(old, new2, expand=True, extractors=e))

w1 = WildcardDict({('insert_list', '*'): SequenceWrapper(),
                   ('change_list', '*'): SequenceWrapper()})

w2 = WildcardDict({('insert_list', '*'): SequenceWrapper(),
                   ('change_list', '*'): SequenceWrapper()})

wrap1 = list(wrap(diff1, w1))
wrap2 = list(wrap(diff2, w2))

conflicts = list(get_conflicts(wrap1, wrap2))

def take_left(patch1, patch2, patches1, patches2, ai):
    patch1['take'] = range(len(patch1['patches']))
    patch2['take'] = []

    return True

actions = WildcardDict({('foo',): take_left,
                        ('change_list', '*'): take_left})

uc = resolve(wrap1, wrap2, conflicts, actions)

result = list(unify(wrap1, wrap2, conflicts))
