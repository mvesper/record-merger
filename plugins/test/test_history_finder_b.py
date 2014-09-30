from plugnplay import Plugin
from plugins.pnp_interfaces import HistoryFinderInterface


class HistoryFinderB(Plugin):
    implements = [HistoryFinderInterface]
    source = 'b'

    def __init__(self):
        pass

    def find_history(self, record):
         return [open('/home/mvesper/MasterThesis/record-merger/test/records/b/content1.xml').read()]

