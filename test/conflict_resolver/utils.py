'''
What do we need here:
    1. Two patches that auto resolve                    par
    2. Two other patches that need a rule               pr
    3. Two other patches that need a lower level rule   plr
    4. Two list patches that auto resolve               lpar
    5. Three sets of list patches that conflict         lp
'''

# 1
par_l = {'action': 'change',
         'path': ('auto_resolve',),
         'value': {'from': 'foo', 'to': 'bar'},
         'group': None}
par_r = {'action': 'change',
         'path': ('auto_resolve',),
         'value': {'from': 'foo', 'to': 'bar'},
         'group': None}

# 2
pr_l = {'action': 'change',
        'path': ('direct_rule',),
        'value': {'from': 'foo', 'to': 'bar'},
        'group': None}
pr_r = {'action': 'change',
        'path': ('direct_rule',),
        'value': {'from': 'foo', 'to': 'banana'},
        'group': None}

# 3
plr_l = {'action': 'change',
         'path': ('indirect_rule',),
         'value': {'from': 'foo', 'to': 'bar'},
         'group': None}
plr_r = {'action': 'change',
         'path': ('indirect_rule',),
         'value': {'from': 'foo', 'to': 'banana'},
         'group': None}

# 4
lpar_l1 = {'action': 'change',
           'path': ('list1', 0),
           'value': {'from': 'foo', 'to': 'bar'},
           'group': 1}
lpar_l2 = {'action': 'change',
           'path': ('list1', 1),
           'value': {'from': 'apple', 'to': 'banana'},
           'group': 1}

lpar_r1 = {'action': 'change',
           'path': ('list1', 0),
           'value': {'from': 'foo', 'to': 'bar'},
           'group': 0}
lpar_r2 = {'action': 'change',
           'path': ('list1', 1),
           'value': {'from': 'apple', 'to': 'banana'},
           'group': 0}


# 5
lp_l11 = {'action': 'change',
          'path': ('list2', 0),
          'value': {'from': 'foo', 'to': 'bar'},
          'group': 1}
lp_l12 = {'action': 'change',
          'path': ('list2', 1),
          'value': {'from': 'apple', 'to': 'banana'},
          'group': 1}

lp_r11 = {'action': 'change',
          'path': ('list2', 1),
          'value': {'from': 'apple', 'to': 'pineapple'},
          'group': 0}
lp_r12 = {'action': 'change',
          'path': ('list2', 2),
          'value': {'from': 'mango', 'to': 'maracuya'},
          'group': 0}
lp_r13 = {'action': 'change',
          'path': ('list2', 3),
          'value': {'from': 'strawberry', 'to': 'raspberry'},
          'group': 0}

lp_l21 = {'action': 'change',
          'path': ('list2', 3),
          'value': {'from': 'strawberry', 'to': 'blueberry'},
          'group': 2}
lp_l22 = {'action': 'change',
          'path': ('list2', 4),
          'value': {'from': 'pear', 'to': 'passion fruit'},
          'group': 2}

patches1 = [par_l, pr_l, plr_l, lpar_l1, lpar_l2, lp_l11, lp_l12, lp_l21, lp_l22]
patches2 = [par_r, pr_r, plr_r, lpar_r1, lpar_r2, lp_r11, lp_r12, lp_r13]

conflicts = [([{'action': 'change',
                'group': None,
                'path': ('auto_resolve',),
                'value': {'from': 'foo', 'to': 'bar'}}],
              [{'action': 'change',
                'group': None,
                'path': ('auto_resolve',),
                'value': {'from': 'foo', 'to': 'bar'}}]),
             ([{'action': 'change',
                'group': None,
                'path': ('direct_rule',),
                'value': {'from': 'foo', 'to': 'bar'}}],
              [{'action': 'change',
                'group': None,
                'path': ('direct_rule',),
                'value': {'from': 'foo', 'to': 'banana'}}]),
             ([{'action': 'change',
                'group': None,
                'path': ('indirect_rule',),
                'value': {'from': 'foo', 'to': 'bar'}}],
              [{'action': 'change',
                'group': None,
                'path': ('indirect_rule',),
                'value': {'from': 'foo', 'to': 'banana'}}]),
             ([{'action': 'change',
                'conflicted': True,
                'environment': 'list',
                'group': 1,
                'path': ('list1', 0),
                'value': {'from': 'foo', 'to': 'bar'}},
               {'action': 'change',
                'conflicted': True,
                'environment': 'list',
                'group': 1,
                'path': ('list1', 1),
                'value': {'from': 'apple', 'to': 'banana'}}],
              [{'action': 'change',
                'conflicted': True,
                'environment': 'list',
                'group': 0,
                'path': ('list1', 0),
                'value': {'from': 'foo', 'to': 'bar'}},
               {'action': 'change',
                'conflicted': True,
                'environment': 'list',
                'group': 0,
                'path': ('list1', 1),
                'value': {'from': 'apple', 'to': 'banana'}}]),
             ([{'action': 'change',
                'conflicted': True,
                'environment': 'list',
                'group': 1,
                'path': ('list2', 0),
                'value': {'from': 'foo', 'to': 'bar'}},
               {'action': 'change',
                'conflicted': True,
                'environment': 'list',
                'group': 1,
                'path': ('list2', 1),
                'value': {'from': 'apple', 'to': 'banana'}},
               None,
               None],
              [None,
               {'action': 'change',
                'conflicted': True,
                'environment': 'list',
                'group': 0,
                'path': ('list2', 1),
                'value': {'from': 'apple', 'to': 'pineapple'}},
               {'action': 'change',
                'conflicted': True,
                'environment': 'list',
                'group': 0,
                'path': ('list2', 2),
                'value': {'from': 'mango', 'to': 'maracuya'}},
               {'action': 'change',
                'conflicted': True,
                'environment': 'list',
                'group': 0,
                'path': ('list2', 3),
                'value': {'from': 'strawberry', 'to': 'raspberry'}}]),
             ([None,
               None,
               {'action': 'change',
                'conflicted': True,
                'environment': 'list',
                'group': 2,
                'path': ('list2', 3),
                'value': {'from': 'strawberry', 'to': 'blueberry'}},
               {'action': 'change',
                'conflicted': True,
                'environment': 'list',
                'group': 2,
                'path': ('list2', 4),
                'value': {'from': 'pear', 'to': 'passion fruit'}}],
              [{'action': 'change',
                'conflicted': True,
                'environment': 'list',
                'group': 0,
                'path': ('list2', 1),
                'value': {'from': 'apple', 'to': 'pineapple'}},
               {'action': 'change',
                'conflicted': True,
                'environment': 'list',
                'group': 0,
                'path': ('list2', 2),
                'value': {'from': 'mango', 'to': 'maracuya'}},
               {'action': 'change',
                'conflicted': True,
                'environment': 'list',
                'group': 0,
                'path': ('list2', 3),
                'value': {'from': 'strawberry', 'to': 'raspberry'}},
               None])]

def assign_list_environment(patches):
    for patch in patches:
        if patch['group'] is not None:
            patch['environment'] = 'list'
