from plugins.pnp_interfaces import (SourceFinderInterface,
                                    InternalConverterInterface,
                                    OriginalConverterInterface,
                                    HistoryFinderInterface,
                                    MergeAction)
import plugnplay

# TODO: Find a superclass for the Managers, since get_* looks the same everywhere...

class SourceFinder:
    def __init__(self):
        self.plugins = SourceFinderInterface.implementors()


class InternalConverter:
    def __init__(self):
        self.plugins = InternalConverterInterface.implementors()

    def get_converter(self, source1, source2=None):
        specific_plugin = []
        general_plugin = []

        for plugin in self.plugins:
            if plugin.source1 == source1:
                if source2 is not None and plugin.source2 == source2:
                    specific_plugin.append(plugin)
                elif plugin.source2 is None:
                    general_plugin.append(plugin)
        
        if specific_plugin:
            return specific_plugin[0]
        elif general_plugin:
            return general_plugin[0]
        else:
            raise Exception('No plugin to convert given record.')


class OriginalConverter:
    def __init__(self):
        self.plugins = OriginalConverterInterface.implementors()

    def get_converter(self, source1, source2=None):
        specific_plugin = []
        general_plugin = []

        for plugin in self.plugins:
            if plugin.source1 == source1:
                if source2 is not None and plugin.source2 == source2:
                    specific_plugin.append(plugin)
                elif plugin.source2 is None:
                    general_plugin.append(plugin)
        
        if specific_plugin:
            return specific_plugin[0]
        elif general_plugin:
            return general_plugin[0]
        else:
            raise Exception('No plugin to convert given record.')


class HistoryFinder:
    def __init__(self):
        self.plugins = HistoryFinderInterface.implementors()

    def get_history_finder(self, source):
        for plugin in self.plugins:
            if plugin.source == source:
                return plugin

        raise Exception('No plugin to find the history of given record')


class MergeActionFinder:
    def __init__(self):
        self.plugins = MergeAction.implementors()

    def get_actions(self, source1, source2=None):
        specific_plugin = []
        general_plugin = []

        for plugin in self.plugins:
            if plugin.source1 == source1:
                if source2 is not None and plugin.source2 == source2:
                    specific_plugin.append(plugin)
                elif plugin.source2 is None:
                    general_plugin.append(plugin)
        
        if specific_plugin:
            return specific_plugin[0]
        elif general_plugin:
            return general_plugin[0]
        else:
            raise Exception('No merge rules for given records.')


plugnplay.plugin_dirs = ['plugins']
plugnplay.load_plugins()

