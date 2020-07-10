## Build query inside an area

```
Build query inside an area (quickosm:buildqueryinsidearea)

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

AREA: Inside the area

	Parameter type:	QgsProcessingParameterString

	Accepted data types:
		- str
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
