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

# The order is important. The first server will be the default.
OVERPASS_SERVERS = [
    'http://www.overpass-api.de/api/',
    'http://overpass.osm.rambler.ru/cgi/',
    'http://api.openstreetmap.fr/oapi/',
    'http://overpass.osm.ch/api/',
    'https://overpass.kumi.systems/api/',
]
