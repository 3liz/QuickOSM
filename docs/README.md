---
Title: QuickOSM
Favicon: icon.png
...

# Documentation

* [Processing](./processing/)
* [Source code](./dev)

# Tutorial using the GUI

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

# Tutorial using a Processing model or a Python script

For the documentation about Processing algorithm, read [Processing](./processing/).

Since QGIS 3.4, QuickOSM is available in the Processing modeler.
Here some useful algorithms in an appropriate order:

* **QuickOSM** → **Advanced**, one of the **Build query** algorithms.
* **File Tools** → **Download file**, by using the `Encoded URL` as a input parameter from the previous algorithm.
* To process the OSM file : 
    * Either **Modeler Tools** → **String concatenation**.
    Useful to concatenate the downloaded filepath with
      * `|layername=points`
      * `|layername=lines`
      * `|layername=multilinestrings`
      * `|layername=multipolygons`
    * Or **QuickOSM** → **Open OSM file**. Instead of the step above with the string concatenation.
* Then it's up to you to combine other QGIS algorithms.

Check a more detailed answer on [stackexchange](https://gis.stackexchange.com/a/313360/24505) :

* **Vector Table** → **Explode HStore field** (QGIS ≥ 3.6)
* **Vector Table** → **Feature filter**

Since QGIS 3.6, you can export your Processing model as a Python script.

As an example, you can download [this model](https://github.com/3liz/QuickOSM/blob/master/QuickOSM/resources/model/osm_download_style.model3) and
[load it in your QGIS](https://docs.qgis.org/3.10/en/docs/user_manual/processing/modeler.html#saving-and-loading-models).
Additionally, you can download example QGIS style files for OSM from [here](https://github.com/anitagraser/QGIS-resources/tree/master/qgis2/osm_spatialite).
The model will download and style OSM data from an extent and packages it in one Geopackage.
