# QuickOSM

![Logo of QuickOSM](QuickOSM/resources/icons/QuickOSM.svg)

[![Build Status](https://api.travis-ci.org/3liz/QuickOSM.svg?branch=master)](https://travis-ci.org/3liz/QuickOSM)

## Versions

* QuickOSM is maintained only for a maintained QGIS version (LTR, stable release and dev).

| QuickOSM  | QGIS Min | QGIS Max | Branch       |
|-----------|----------|----------|--------------|
| 1.0 → 1.4 | 2.0      | 2.18     | [master_qgis2](https://github.com/3liz/QuickOSM/tree/master_qgis2) |
| 1.5 → 1.7 | 3.0      | 3.2      |              |
| 1.8 →     | 3.4      |          | [master](https://github.com/3liz/QuickOSM/tree/master)       |

## Documentation

The user guide, and the developer guide are available https://docs.3liz.org/QuickOSM/

## Generalities

QuickOSM allows you to work quickly with OSM data in QGIS thanks to [Overpass API][Overpass].
* Write some queries for you by providing a key/value
* Choose to run the query on an area or an extent
* Configure the query : which layers, which columns…
* Open a local OSM (.osm or .pbf) with a specific osmconf in QGIS
* Build some models with QGIS Processing

There are some useful tips, like automatic colours on lines (if the tag is present),
or some actions (right-click in the attribute table) for each entity (edit in JOSM for instance).

[Overpass]: https://wiki.openstreetmap.org/wiki/Overpass_API

## Translation

* The web-based translating platform [Transifex](https://www.transifex.com/quickosm/gui/dashboard/) is used.

## Credits

Author: Etienne Trimaille : https://twitter.com/etrimaille

Contributors:
* Richard Marsden [winwaed](https://github.com/winwaed)
