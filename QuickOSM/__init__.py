"""QuickOSM plugin init."""

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'


# noinspection PyDocstring,PyPep8Naming
def classFactory(iface):
    from QuickOSM.quick_osm import QuickOSMPlugin
    return QuickOSMPlugin(iface)
