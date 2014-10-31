from ConfigParser import ConfigParser
from patch_extractor.utils import KeyLimit
from utils import WildcardDict


class ConfigManager(object):
    def __init__(self, config_path, actions_path=None):
        with open(config_path) as f:
            config = ConfigParser()
            config.readfp(f)

        self._key_limits = set()
        self._filter_actions = WildcardDict()
        self._conflict_actions = WildcardDict()

        if actions_path is None:
            action_path = config_path.replace('.conf', '.py')
        self._actions = self._load_actions(action_path)

        for path, action in config.items('FILTERING'):
            _path = tuple(path.split(', '))
            self._key_limits.add(_path)
            self._filter_actions[_path] = self._actions[action]

        for path, action in config.items('CONFLICTS'):
            _path = tuple(path.split(', '))
            self._key_limits.add(_path)
            self._conflict_actions[_path] = self._actions[action]

        self._key_limits = KeyLimit(self._key_limits)

    def _load_actions(self, actions_path):
        _locals = {}
        execfile(actions_path, {}, _locals)
        return _locals

    def get_key_limits(self):
        return self._key_limits

    def get_filter_actions(self):
        return self._filter_actions

    def get_conflict_actions(self):
        return self._conflict_actions
