# Changelog

## Unreleased

* Fix Python exception if the user input is not recognised as a valid preset
* Update default JOSM/Vespucci presets from 2.9.0 to 4.1.2

## 2.0.1 - 2022-02-07

* Fix trunk roads to Urban visualization preset (contribution from @Rikuoja)
* Fix an error when running Python 3.10

## 2.0.0 - 2021-09-09

* Release of QuickOSM 2.0.0
* Add Vietnamese language
* Update of translations https://docs.3liz.org/QuickOSM/translation-stats/
  * Chinese, Dutch, French, Indonesian, Italian are now fully translated, thanks to contributors
* Raise minimum version to QGIS 3.16
* Add presets for the keys/values
* Add multi-keys query from Quick Query panel
* Add history of queries
* Add option to get the metadata of OSM data such as author, timestamp etc
* Add default map presets to download a map with many queries
* Add a button to save the query in a personal preset (new or existing one)
* Add an action to reload the query
* Add processing algorithms for the "Quick Query", available in the QGIS Processing toolbox
* Add several output format such as Geopackage, KML
* Add the possibility to load only a subset of a local file
* Boost of performance using HStore processing algorithm to parse the downloaded OSM file
* Improve user interface
* Update of the documentation

## 2.0.0-beta4 - 2021-09-01

* Fix the query might be too long for the server when using a GET request by reducing the number of decimals
* Fix issue about reprojection of bounding box when using QuickOSM in QGIS Processing
* Update of translations https://docs.3liz.org/QuickOSM/translation-stats/ 
  * Chinese, Dutch, French, Indonesian, Italian are now fully translated, thanks to contributors

## 2.0.0-beta3 - 2021-08-12

* Fix the selection of the preset to run
* Fix the opening of an osm file with a custom configuration file
* Fix the reset of the dialog

## 2.0.0-beta2 - 2021-08-06

* Update the translations
* Add some documentations for users and for developers
* Add the preset translations in zip
* Fix the selection of preset

## 2.0.0-beta1 - 2021-08-02

* Raise minimum version to QGIS 3.16
* Add presets for the keys/values
* Add multi-keys query from Quick Query panel
* Add history of queries
* Add option to get the metadata of OSM data such as author, timestamp etc
* Add default map presets to download a map with many queries
* Add a button to save the query in a personal preset (new or existing one)
* Add an action to reload the query
* Add processing algorithms for the "Quick Query"
* Add several output format such as geopackage, KML
* Add the possibility to load only a subset of a local file
* Boost of performance using HStore processing algorithm to parse the downloaded OSM file
* Improve user interface
* Update of the documentation

## 1.17.1 - 2021-06-23

* Add a reminder of the copyrights
* Fix loading of translations files
* Fix an error triggered when there was no layer in the project that prevented the generation functionality
* Fix an error when using QuickOSM in a Processing model

## 1.17.0 - 2021-06-09

* Add OpenHistoricalMap overpass server, linked to https://www.openhistoricalmap.org
* Add an option to use the extent of selected features
* Add Overpass Query Language (OQL) generator by default instead of legacy XML
* Add the possibility to choose the Nominatim server, by default the one from qgis.org
* Add one check from the Overpass API if too many requests from the user
* Fix the Mapillary action in the attribute table
* Fix some user experience issue about the place name
* Fix user experience about the named area drop-down menu
* Fix 'Around' query type to fetch any OSM object instead of only OSM nodes.  
* In the source code, add some Python annotations and more tests

## 1.16.0 - 2021-03-26

* Changelog from 1.15.0 which has been unapproved
* Avoid regression from 1.15.0 about empty attribute table
* Always check to open file with UTF8

## 1.15.0 - 2021-03-10

* Fix the button to "show the query"
* Fix QGIS Processing algorithm about GDAL parameter
* Add the OSM key "aeroway"
* Add a button to open the online help from the QGIS help menu
* Update the documentation with a proper website https://docs.3liz.org/QuickOSM/
* Add an automatic documentation for QGIS Processing algorithms on the website
* Some Python automatic code review

## 1.14.3 - 2020-09-18

* Fix issue about unicode in the OSM file when reading the end of the file only #240

## 1.14.2 - 2020-01-30

* Fix railway=abandoned
* Add a model by default in the modeler
* Fix loading translation file

## 1.14.1 - 2019-11-23

* Update translations from Transifex
* Fix bug #220 about loading local OSM file with custom config
* Add section about code contributors

## 1.14.0 - 2019-11-11

* Version 1.13.X was only experimental, so all features from 1.13.X
* Show human friendly label in the QuickQuery
