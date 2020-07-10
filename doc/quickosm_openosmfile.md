## Open sublayers from an OSM file

```
Open sublayers from an OSM file (quickosm:openosmfile)

Open all sublayers from an OSM file. A custom OSM configuration file can be specified following the OGR documentation. This algorithm will not make a copy of the input file, it will only open it using OGR and custom INI file if provided.


----------------
Input parameters
----------------

FILE: OSM file

	Parameter type:	QgsProcessingParameterFile

	Accepted data types:
		- str
		- QgsProperty

OSM_CONF: OSM configuration

	Parameter type:	QgsProcessingParameterFile

	Accepted data types:
		- str
		- QgsProperty

----------------
Outputs
----------------

OUTPUT_POINTS:  <QgsProcessingOutputVectorLayer>
	Output points

OUTPUT_LINES:  <QgsProcessingOutputVectorLayer>
	Output lines

OUTPUT_MULTILINESTRINGS:  <QgsProcessingOutputVectorLayer>
	Output multilinestrings

OUTPUT_MULTIPOLYGONS:  <QgsProcessingOutputVectorLayer>
	Output multipolygons

OUTPUT_OTHER_RELATIONS:  <QgsProcessingOutputVectorLayer>
	Output other relations
```
