def pick_left(patches1, patches2, _1, _2, _3):
    for p in patches1:
        try:
            p['take'] = True
        except:
            pass
    for p in patches2:
        try:
            p['take'] = False
        except:
            pass

    return True

