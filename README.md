# QuickOSM

![Logo of QuickOSM](resources/icons/QuickOSM.svg)

## Versions

* QuickOSM is maintained only for a maintained QGIS version (LTR, stable release and dev).
* Current test status master on QGIS Master and LTR : [![Build Status](https://api.travis-ci.org/3liz/QuickOSM.svg?branch=master)](https://travis-ci.org/3liz/QuickOSM)

| QuickOSM  | QGIS Min | QGIS Max | Branch       |
|-----------|----------|----------|--------------|
| 1.0 → 1.4 | 2.0      | 2.18     | [master_qgis2](https://github.com/3liz/QuickOSM/tree/master_qgis2) |
| 1.5 → 1.7 | 3.0      | 3.2      |              |
| 1.8 →     | 3.4      |          | [master](https://github.com/3liz/QuickOSM/tree/master)       |

#### Watch the [Video tutorial](https://vimeo.com/108737868)

**Install the QuickOSM plugin**
* QGIS `Plugins` menu → `Manage and Install Plugins…`
* Search for `QuickOSM` and select it
* `Install Plugin`

**Try a quick query**
* `Vector` menu → `QuickOSM` -> `QuickOSM`
* In the `key` field enter `amenity`
* In the `value` field enter `toilets`
* Set the name of the town/village to `London`
* `Run Query`

The Overpass API takes a few seconds to respond, and after that you should get new 
point and polygon layers for the toilets of London! (nodes and ways in OpenStreetMap 
with the `amenity`=`toilet` tag on them) 


## Generalities

QuickOSM allows you to work quickly with OSM data in QGIS thanks to [Overpass API][Overpass].
* Write some queries for you by providing a key/value
* Choose to run the query on an area or an extent
* Configure the query : which layers, which columns…
* Open a local OSM (.osm or .pbf) with a specific osmconf in QGIS
* Build some models with QGIS Processing

There are some useful tips, like automatic colours on lines (if the tag is present)
 or some actions (right-click in the attribute table) for each entities (edit in JOSM for instance).

[Overpass]: https://wiki.openstreetmap.org/wiki/Overpass_API

## Using QuickOSM in a Processing model or in a Python script

Since QGIS 3.4, QuickOSM is available in the Processing modeler.
Here some useful algorithms in an appropriate order:
* **QuickOSM** → **Advanced**, one of the **Build query** algorithms.
* **File Tools** → **Download file**.
* **Modeler Tools** → **String concatenation**. 
Useful to concatenate the downloaded filepath with
  * `|layername=points`
  * `|layername=lines`
  * `|layername=multilinestrings`
  * `|layername=multipolygons`
* **QuickOSM** → **Open OSM file**. Instead of the step above with the string concatenation.
 
Check a more detailed answer on [stackexchange](https://gis.stackexchange.com/a/313360/24505).
* **Vector Table** → **Explode HStore field** (QGIS ≥ 3.6)
* **Vector Table** → **Feature filter**

Since QGIS 3.6, you can export your Processing model as a Python script.

## Development

For panels, you can find a quick diagram in the `doc` folder.

## Authors

Etienne Trimaille : https://twitter.com/etrimaille