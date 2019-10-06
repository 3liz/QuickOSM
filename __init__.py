"""QuickOSM plugin init."""

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'


# noinspection PyDocstring,PyPep8Naming
def classFactory(iface):
    from .quick_osm import QuickOSMPlugin
    return QuickOSMPlugin(iface)


# noinspection PyDocstring,PyPep8Naming
# def serverClassFactory(serverIface):
    # noinspection PyUnresolvedReferences
    # from .quick_osm_processing.provider import Provider
    # pass
