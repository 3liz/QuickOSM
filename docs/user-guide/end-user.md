# Using the GUI

Watch the [Video tutorial](https://vimeo.com/108737868)

**Install the QuickOSM plugin** :

* QGIS `Plugins` menu → `Manage and Install Plugins…`
* Search for `QuickOSM` and select it
* `Install Plugin`

**Try a quick query** :

* `Vector` menu → `QuickOSM` -> `QuickOSM`
* In the `key` field enter `amenity`
* In the `value` field enter `toilets`
* Set the name of the town/village to `London`
* `Run Query`

The Overpass API takes a few seconds to respond, and after that you should get new
point and polygon layers for the toilets of London! (nodes and ways in OpenStreetMap
with the `amenity`=`toilet` tag on them)
