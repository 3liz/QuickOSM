## Build query around an area

```
Build query around an area (quickosm:buildqueryaroundarea)

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

AREA: Around the area (Point WKT accepted)

	Parameter type:	QgsProcessingParameterString

	Accepted data types:
		- str
		- QgsProperty

DISTANCE: Distance (meters)

	Parameter type:	QgsProcessingParameterNumber

	Accepted data types:
		- int
		- float
		- QgsProperty

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
