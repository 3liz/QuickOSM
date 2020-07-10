## Build query inside an extent

```
Build query inside an extent (quickosm:buildqueryextent)

This algorithm builds a query and then encode it into the Overpass API URL. The "Download File" algorithm might be used after that to fetch the result.


----------------
Input parameters
----------------

KEY: Key, default to all keys

	Parameter type:	QgsProcessingParameterString

	Accepted data types:
		- str
		- QgsProperty

VALUE: Value, default to all values

	Parameter type:	QgsProcessingParameterString

	Accepted data types:
		- str
		- QgsProperty

EXTENT: Extent

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

TIMEOUT: Timeout

	Parameter type:	QgsProcessingParameterNumber

	Accepted data types:
		- int
		- float
		- QgsProperty

SERVER: Overpass server

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
