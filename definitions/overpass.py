"""List of Overpass servers.

This file mustn't be modified by users. This file is updated with the plugin.

If you want to add some customs servers, add a file called 'custom_config.json'
in your profile_name/QuickOSM folder and add this template in it:

{
    "overpass_servers": [
        "http://your_custom_url.com/api/"
    ]
}

QuickOSM will add your custom list to the list below.

A pull request is more than welcome if you want to add your server in QuickOSM
core by updating this list below.
"""

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'


# The order is important. The first server will be the default.
OVERPASS_SERVERS = [
    'https://lz4.overpass-api.de/api/',
    'https://z.overpass-api.de/api/',
    'https://overpass.kumi.systems/api/',
    'https://overpass.nchc.org.tw/api/',
    'https://overpass.openstreetmap.fr/api/',
    'http://overpass.osm.ch/api/',
]
