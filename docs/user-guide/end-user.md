# Using the GUI

## Map features

To have an overview of all keys and values, have a look to the OpenStreetMap
[wiki page](https://wiki.openstreetmap.org/wiki/Map_features).

!!! tip
    You can write what ever you want in the `Key` and `Value` fields. OSM data
    model doesn't restrict any keys or values.

!!! tip
    If you want to query **all** data, you can let key and value empty.

## Video

(Outdated) Watch the [Video tutorial](https://vimeo.com/108737868)

## Quick how to

#### Install the QuickOSM plugin :

* QGIS `Plugins` menu → `Manage and Install Plugins…`
* Search for `QuickOSM` and select it
* `Install Plugin`

#### Try a quick query :

* `Vector` menu → `QuickOSM` → `QuickOSM`
* In the `key` field enter `amenity`
* In the `value` field enter `toilets`
* Set the name of the town/village to `London`
* `Run Query`

The Overpass API takes a few seconds to respond, and after that you should get new
point and polygon layers for the toilets of London! (nodes and ways in OpenStreetMap
with the `amenity`=`toilet` tag on them)

#### Try to run a preset

* `Vector` menu → `QuickOSM` → `QuickOSM`
* Go in `Map preset` panel
* Click on preset named `Urban`
* Set the name of the town/village to `Montpellier`
* `Run preset`

The Overpass API takes a few seconds to respond, and after that you should get new
lines and polygon layers that match roads and buildings in Montpellier
with a custom style.

#### Try to save and edit a preset

* `Vector` menu → `QuickOSM` → `QuickOSM`
* In the `key` field enter `amenity`
* In the `value` field enter `theater`
* Set the name of the town/village to `Paris`
* `Save query in a new preset`
* Click on `edit` button in preset named `amenity_theater_Paris`
* In the `preset name` field enter `Culture`
* In the `description` field enter `Theater and museum in Paris`
* `Add anew query`
* Right click on `Query2` → `Rename` → enter `Museum`
* In the `Layer name` field enter `tourism_museum_Paris`  
* In the `key` field enter `tourism`
* In the `value` field enter `museum`
* In the `area` field enter `Paris`
* `Validate`

You now have a preset that download the theaters and then the museums.
You don't need to fill the parameter to run the preset, but you can
if you want the theaters and museums in another place than Paris. 

## Custom API server

If you want to add some customs servers, add a file called `custom_config.json`
in your `profile_name/QuickOSM` folder and add this template in it :
```json
{
    "overpass_servers": [
        "http://your_custom_url.com/api/"
    ],
    "nominatim_servers": [
        "http://your_custom_url.com/search?"
    ]
}
```
Both `overpass_servers` et `nominatim_servers` are optionals. If you want to add only 
one of them, you don't need to write the other.
QuickOSM will add your custom list to the list below.

To find the profile folder, go in **Settings → Profile → Open active profile folder**.

!!! warning
    Do not change any files in `profile_name/python/plugins/QuickOSM` for
    adding a server. Your changes will be lost everytime the plugin is upgraded.

A pull request is more than welcome if you want to add your server in QuickOSM
core by updating this list below.
