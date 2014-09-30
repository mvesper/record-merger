from plugnplay import Plugin
from plugins.pnp_interfaces import SourceFinderInterface

class LocalSourceFinder(Plugin):
    implements = [SourceFinderInterface,]

    def find_source(record):
        return 'local'
