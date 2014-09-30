from plugin_facade import (SourceFinder,
                           InternalConverter,
                           OriginalConverter,
                           HistoryFinder)

from patch_extractor.dict_patch_extractor import DictPatchExtractor
from patch_extractor.list_patch_extractor import ListPatchExtractor


class Record:
    def __init__(self, record, source=None):
        self.original_records = [record]
        self.internal_records = []
        self.source = source
        self.record_patches = []

    def prepare_record(self, other_source=None):
        try:
            if not self.source:
                self.source = self._find_source()
            self.original_records.extend(self._get_record_change_history())
            # Change all the records to the internal format
            for record in self.original_records:
                internal_record = self.convert_to_internal_format(record,
                                                                  other_source)
                self.internal_records.append(internal_record)
            '''
            This is probably not the right place to calculate the diffs... first the
            latest common ancestor should be found
            # Extract the applied patches (using dictdiffer)
            tmp = [x for x in reversed(self.internal_records)]
            for older, newer in zip(tmp[:-1], tmp[1:]):
                extractors = [DictPatchExtractor, ListPatchExtractor]
                extractor = DictPatchExtractor(older, newer,
                                               patch_extractors=extractors)
                self.record_patches.append(extractor.patches)
            '''
        except:
            # reset everything (maybe not really necessary thouge)
            self.original_records = [self.original_records[0]]
            self.internal_records = []
            raise

    def find_source(self):
        for plugin in SourceFinder().plugins:
            source = plugin.find_source(self.record)
            if source:
                return source
        else:
            raise Exception('Could not find a source for the record.')

    def convert_to_internal_format(self, record, other_source=None):
        return (InternalConverter()
                .get_converter(self.source, other_source)
                .convert(record))

    def convert_to_original_format(self, record, other_source=None):
        return (OriginalConverter()
                .get_converter(self.source, other_source)
                .convert(record))

    def _get_record_change_history(self):
        return (HistoryFinder()
                .get_history_finder(self.source)
                .find_history(self.original_records[0]))


