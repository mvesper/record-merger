from plugnplay import Interface

class SourceFinderInterface(Interface):
    def find_source(self, record):
        pass


class InternalConverterInterface(Interface):
    def convert(self, record):
        pass


class OriginalConverterInterface(Interface):
    def convert(self, record):
        pass


class HistoryFinderInterface(Interface):
    pass


class MergeAction(Interface):
    pass

