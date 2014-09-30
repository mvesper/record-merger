from plugnplay import Plugin
from plugins.pnp_interfaces import MergeAction

# TODO: Thoughts about rules...
# The rules are probably compiled with the thought in mind that source1 is the destination,
# so every patch from from source1 should be valid...
#
# Maybe two different types of rules?
#   * One set to compare
#   * Other set to filter changes from 


def bla(_):
    return True


def blub(_):
    return True


class TestMergeRules(Plugin):
    implements = [MergeAction]
    source1 = 'a'
    source2 = 'b'

    def get_action(self, action_name):
        try:
            return globals()[action_name]
        except:
            raise Exception('Function is not defined...')
