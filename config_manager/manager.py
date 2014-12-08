from ConfigParser import ConfigParser
from patch_extractor.utils import KeyLimit
from utils import WildcardDict


class ConfigFormatException(Exception):
    pass


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
            _path = self._parse_path(path)
            self._key_limits.add(_path)
            self._filter_actions[_path] = self._prepare_action(action)

        for path, action in config.items('CONFLICTS'):
            _path = self._parse_path(path)
            self._key_limits.add(_path)
            self._conflict_actions[_path] = self._actions[action]

        self._key_limits = KeyLimit(self._key_limits)

    def _load_actions(self, actions_path):
        _locals = {}
        execfile(actions_path, {}, _locals)
        return _locals

    def _create_function(self, action, if_actions):
        def combined_filter_function(*args, **kwargs):
            if all(map(lambda x: x(*args, **kwargs), if_actions)):
                return action(*args, **kwargs)
            else:
                return True

        return combined_filter_function

    def _prepare_action(self, action):
        # Is there any value in reimplementing an annotation? Probably not, so maybe we should build
        # something else here...
        actions = action.split(' ')
        if len(actions) == 1:
            return self._actions[actions[0]]
        else:
            action = self._actions[actions[-1]]
            if_actions = map(lambda x: self._actions[x], actions[:-1])
            return self._create_function(action, if_actions)

    def _cast(self, value):
        try:
            return int(value)
        except ValueError:
            return value

    def _parse_path(self, path):
        # For our specific use case, we only need strings and ints
        return tuple([self._cast(x) for x in  path.split(', ')])

    def get_key_limits(self):
        return self._key_limits

    def get_filter_actions(self):
        return self._filter_actions

    def get_conflict_actions(self):
        return self._conflict_actions

