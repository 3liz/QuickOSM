# QuickOSM 2, QGIS 3
For the port/rewrite, see the `master_q3` branch: https://github.com/3liz/QuickOSM/tree/master_q3

QuickOSM
============================================================
* Current test status master : [![Build Status](https://travis-ci.org/3liz/QuickOSM.svg)](https://travis-ci.org/3liz/QuickOSM)

Generalities
=
QuickOSM allows you to work quickly with OSM data in QGIS thanks to [Overpass API][Overpass].
* Write some queries for you by providing a key/value
* Choose to run the query on an area or an extent
* Configure the query : which layers, which columns ...
* Save your queries in categories and run them later
* Open a local OSM (.osm or .pbf) with a specific osmconf in QGIS
* Build some models with QGIS Processing

There are some useful tips, like automatic colours on lines (if the tag is present) or some actions (right-click in the attribute table) for each entities (edit in JOSM for instance).

[Overpass]: https://wiki.openstreetmap.org/wiki/Overpass_API

Authors
=
Etienne Trimaille : https://twitter.com/etrimaille

This internship was supervised by 3Liz : http://www.3liz.com

Getting started
=

#### Watch the [Video tutorial](https://vimeo.com/108737868)

**Install the QuickOSM plugin**
* QGIS 'Plugins' menu -> 'Manage and Install Plugins...'
* Search for 'QuickOSM' and select it
* 'Install Plugin'

**Try a quick query**
* 'Vector' menu -> 'Quick OSM' -> 'Dock -> 'Quick Query'

a new panel appears on the right
* In the 'key' field enter 'amenity'
* In the 'value' field enter 'toilets'
* Set the name of the town/village to 'London'
* 'Run Query'

The Overpass API takes a few seconds to respond, and after that you should get new point and polygon layers for the toilets of London! (nodes and ways in OpenStreetMap with the amenity=toilet tag on them) 

