# QuickOSM

![Logo of QuickOSM](QuickOSM/resources/icons/QuickOSM.svg)

[![QGIS.org](https://img.shields.io/badge/QGIS.org-published-green)](https://plugins.qgis.org/plugins/QuickOSM/)
[![Documentation 📚](https://github.com/3liz/QuickOSM/actions/workflows/publish-doc.yml/badge.svg)](https://github.com/3liz/QuickOSM/actions/workflows/publish-doc.yml)
[![Tests 🎳](https://github.com/3liz/QuickOSM/actions/workflows/ci.yml/badge.svg)](https://github.com/3liz/QuickOSM/actions/workflows/ci.yml)
[![Transifex 🗺](https://github.com/3liz/QuickOSM/actions/workflows/transifex.yml/badge.svg)](https://github.com/3liz/QuickOSM/actions/workflows/transifex.yml)

## Versions

* QuickOSM is maintained only for a maintained QGIS version (LTR, stable release and dev).

| QuickOSM    | QGIS Min | QGIS Max | Branch                                                             |
|-------------|----------|------|--------------------------------------------------------------------|
| 1.0 → 1.4   | 2.0      | 2.18 | [master_qgis2](https://github.com/3liz/QuickOSM/tree/master_qgis2) |
| 1.5 → 1.7   | 3.0      | 3.2  |                                                                    |
| 1.8 → 1.17  | 3.4      | 3.14 |                                                                    |
| 2.0 → 2.1.1 | 3.16     | 3.22 |                                                                    |
| 2.2.0 →     | 3.22     |      | [master](https://github.com/3liz/QuickOSM/tree/master)             |

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

Author: Etienne Trimaille : https://mapstodon.space/@etrimaille

Contributors:
* Richard Marsden [winwaed](https://github.com/winwaed)
* Maxime Charzat [mcharzat](https://github.com/mcharzat)
* [Huntani](https://github.com/Huntani)
