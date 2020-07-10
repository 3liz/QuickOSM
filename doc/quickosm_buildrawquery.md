## Build raw query

```
Build raw query (quickosm:buildrawquery)


----------------
Input parameters
----------------

QUERY: Query

	Parameter type:	QgsProcessingParameterString

	Accepted data types:
		- str
		- QgsProperty

EXTENT: Extent, if "{{bbox}}" in the query

	Parameter type:	QgsProcessingParameterExtent

	Accepted data types:
		- str: as comma delimited list of x min, x max, y min, y max. E.g. '4,10,101,105'
		- str: layer ID. Extent of layer is used.
		- str: layer name. Extent of layer is used.
		- str: layer source. Extent of layer is used.
		- QgsMapLayer: Extent of layer is used
		- QgsProcessingFeatureSourceDefinition: Extent of source is used
		- QgsProperty
		- QgsRectangle
		- QgsReferencedRectangle
		- QgsGeometry: bounding box of geometry is used

SERVER: Overpass server

	Parameter type:	QgsProcessingParameterString

	Accepted data types:
		- str
		- QgsProperty

AREA: Area (if you want to override {{geocodeArea}} in the query)

	Parameter type:	QgsProcessingParameterString

	Accepted data types:
		- str
		- QgsProperty

----------------
Outputs
----------------

OUTPUT_URL:  <QgsProcessingOutputString>
	Query as encoded URL

OUTPUT_OQL_QUERY:  <QgsProcessingOutputString>
	Raw query as OQL
```
