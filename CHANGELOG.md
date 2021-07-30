# Changelog

## Unreleased

## 2.0.0 - 2021-07-30

* Add presets for the keys/values
* Add multi-keys query from quick query panel
* Add history of queries
* Add option to get the metadata of osm
* Add default map presets  
* Add save query in a personal preset (new or existing one)
* Add an action to reload the query
* Add processing algorithms
* Add several output format
* Add the possibility to load only a subset of a local file
* Boost of performance using HStore processing algorithm to parse the downloaded osm file
* Improve UI
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
