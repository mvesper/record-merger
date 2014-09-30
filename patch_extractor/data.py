class Patch:
    '''
    Note: 
    Since a patch is about what and where to put it, it might
    be better idea to save the value instead of the  path to
    the new document. This is also going to make the patching
    easier.
    '''
    def __init__(self):
        self.path = []
        self.value = None
        self.action = None

