from pprint import pprint

from record import Record
from merger import merge


xml1 = open('/home/mvesper/MasterThesis/record-merger/test/records/a/content3.xml').read()
xml2 = open('/home/mvesper/MasterThesis/record-merger/test/records/b/content2.xml').read()

record1 = Record(xml1, 'a')
record2 = Record(xml2, 'b')

record1.prepare_record('b')
record2.prepare_record('a')

pprint(merge(record1, record2))
