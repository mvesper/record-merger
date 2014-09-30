from plugnplay import Plugin
from plugins.pnp_interfaces import HistoryFinderInterface


class HistoryFinderA(Plugin):
    implements = [HistoryFinderInterface]
    source = 'a'

    def __init__(self):
        pass

    def find_history(self, record):
         return [open('/home/mvesper/MasterThesis/record-merger/test/records/a/content2.xml').read(),
                 open('/home/mvesper/MasterThesis/record-merger/test/records/a/content1.xml').read()]
