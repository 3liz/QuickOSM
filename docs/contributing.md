---
hide:
  - navigation
---

<!--
The file CONTRIBUTING.md is copied by the CI before building the doc in this directory
On your local, make a symlink with ln -s
-->

--8<-- "./CONTRIBUTING.md"

## Architecture

```mermaid
classDiagram
BasePanel
BaseProcessingPanel
ConfigurationPanel
BaseOverpassPanel
OsmFilePanel
QueryPanel
QuickQueryPanel
BasePanel <|-- BaseProcessingPanel
BasePanel <|-- ConfigurationPanel
BaseProcessingPanel <|-- BaseOverpassPanel
BaseProcessingPanel <|-- OsmFilePanel
BaseOverpassPanel <|-- QueryPanel
BaseOverpassPanel <|-- QuickQueryPanel
class BasePanel{
  <<abstract>>
  +Panel
  +Dialog
}
class BaseProcessingPanel{
  <<abstract>>
  run()
  _run()
  setup_panel()
  _start_process()
  _end_process()
  gather_values()
}
class BaseOverpassPanel{
  <<abstract>>
  last_places
  nominatim()
  end_query()
  gather_values()
}
```
