"""Actions definitions."""

from qgis.core import Qgis, QgsAction
from qgis.utils import iface, plugins

from .utilities.utilities_qgis import open_webpage
from ..qgis_plugin_tools.tools.i18n import tr
from ..qgis_plugin_tools.tools.resources import resources_path

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'


ACTIONS_PATH = 'from QuickOSM.core.actions import Actions;'
ACTIONS_VISIBILITY = ['Canvas', 'Feature', 'Field']


def add_actions(layer, keys):
    """Add actions on layer.

    :param layer: The layer.
    :type layer: QgsVectorLayer

    :param keys: The list of keys in the layer.
    :type keys: list
    """
    actions = layer.actions()

    title = tr('OpenStreetMap Browser')
    osm_browser = QgsAction(
        QgsAction.OpenUrl,
        title,
        'http://www.openstreetmap.org/browse/[% "osm_type" %]/[% "osm_id" %]',
        '',
        False,
        title,
        ACTIONS_VISIBILITY,
        ''
    )
    actions.addAction(osm_browser)

    title = 'Mapillary'
    mapillary = QgsAction(
        QgsAction.GenericPython,
        title,
        ACTIONS_PATH + 'Actions.run("mapillary","[% "mapillary" %]")',
        resources_path('icons', 'mapillary_logo.svg'),
        False,
        title,
        ACTIONS_VISIBILITY,
        ''
    )
    actions.addAction(mapillary)

    title = 'JOSM'
    josm = QgsAction(
        QgsAction.GenericPython,
        title,
        ACTIONS_PATH + 'Actions.run("josm","[% "full_id" %]")',
        resources_path('icons', 'josm_icon.svg'),
        False,
        title,
        ACTIONS_VISIBILITY,
        ''
    )
    actions.addAction(josm)

    title = tr('User default editor')
    default_editor = QgsAction(
        QgsAction.OpenUrl,
        title,
        'http://www.openstreetmap.org/edit?[% "osm_type" %]=[% "osm_id" %]',
        '',
        False,
        title,
        ACTIONS_VISIBILITY,
        ''
    )
    actions.addAction(default_editor)

    for link in ['url', 'website', 'wikipedia', 'wikidata', 'ref:UAI']:
        if link in keys:

            # Add an image to the action if available
            image = ''
            if link == 'wikipedia':
                image = resources_path('icons', 'wikipedia.png')
            elif link == 'wikidata':
                image = resources_path('icons', 'wikidata.png')
            elif link in ['url', 'website']:
                image = resources_path('icons', 'external_link.png')

            link = link.replace(":", "_")
            generic = QgsAction(
                QgsAction.GenericPython,
                link,
                (ACTIONS_PATH
                 + 'Actions.run("{link}","[% "{link}" %]")'.format(link=link)),
                image,
                False,
                link,
                ACTIONS_VISIBILITY,
                ''
            )
            actions.addAction(generic)

    if 'network' in keys and 'ref' in keys:
        sketch_line = QgsAction(
            QgsAction.GenericPython,
            tr('Sketchline'),
            (ACTIONS_PATH +
             'Actions.run_sketch_line("[% "network" %]","[% "ref" %]")'),
            '',
            False,
            '',
            ACTIONS_VISIBILITY,
            ''
        )
        actions.addAction(sketch_line)


class Actions:
    """
    Manage actions available on layers
    """

    @staticmethod
    def run(field, value):
        """
        Run an action with only one value as parameter

        @param field:Type of the action
        @type field:str
        @param value:Value of the field for one entity
        @type value:str
        """

        if value == '':
            iface.messageBar().pushMessage(
                tr('Sorry, the field \'{fieldname}\' is empty for this entity.'
                   .format(fieldname=field)),
                level=Qgis.Warning, duration=7)
        else:

            if field in ['url', 'website', 'wikipedia', 'wikidata']:
                url = None

                if field == 'url' or field == 'website':
                    url = value

                if field == 'ref_UAI':
                    url = "http://www.education.gouv.fr/pid24302/annuaire-" \
                          "resultat-recherche.html?lycee_name=" + value

                if field == 'wikipedia':
                    url = "http://en.wikipedia.org/wiki/" + value

                if field == 'wikidata':
                    url = "http://www.wikidata.org/wiki/" + value

                open_webpage(url)

            elif field == 'mapillary':
                if 'go2mapillary' in plugins:
                    plugins['go2mapillary'].viewer.open(value)
                else:
                    url = 'https://www.mapillary.com/map/im/' + value
                    open_webpage(url)

            elif field == 'josm':
                import urllib.request
                import urllib.error
                import urllib.parse
                try:
                    url = 'http://localhost:8111/load_object?objects=' + value
                    urllib.request.urlopen(url).read()
                except urllib.error.URLError:
                    iface.messageBar().pushMessage(
                        tr('The JOSM remote seems to be disabled.'),
                        level=Qgis.Critical,
                        duration=7)

            # NOT USED
            elif field == 'rawedit':
                # url = QUrl("http://rawedit.openstreetmap.fr/edit/" + value)
                # web_browser = QWebView(None)
                # web_browser.load(url)
                # web_browser.show()
                pass

    @staticmethod
    def run_sketch_line(network, ref):
        """
        Run an action with two values for sketchline

        @param network:network of the bus
        @type network:str
        @param ref:ref of the bus
        @type ref:str
        """
        if network == '' or ref == '':
            iface.messageBar().pushMessage(
                tr('Sorry, this field is empty for this entity.'),
                level=Qgis.Warning,
                duration=7)
        else:
            url = (
                'http://www.overpass-api.de/api/sketch-line?'
                'network={network}&ref={ref}').format(network=network, ref=ref)
            open_webpage(url)
