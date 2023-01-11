# dash-cytoscape-elements
[![test](https://github.com/minefuto/dash-cytoscape-elements/actions/workflows/test.yml/badge.svg)](https://github.com/minefuto/dash-cytoscape-elements/actions/workflows/test.yml)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dash-cytoscape-elements)
![PyPI](https://img.shields.io/pypi/v/dash-cytoscape-elements)
![GitHub](https://img.shields.io/github/license/minefuto/dash-cytoscape-elements)

This is a Python object for [Dash Cytoscape](https://github.com/plotly/dash-cytoscape) Elements.

## Features
- Add/Remove/Get/Filter Element(Node/Edge) on Python object.
- Convert Python object from/to Dash Cytoscape format 
- Convert Python object from/to json(Cytoscape.js format)

## Install
```
pip install dash-cytoscape-elements
```

## Usage
Example1: Create Elements object & using on Dash Cytoscape  
```python
import dash
import dash_cytoscape as cyto
from dash import html
from dash_cytoscape_elements import Elements

elements = Elements()
elements.add(id="one", label="Node 1", x=50, y=50)
elements.add(id="two", label="Node 2", x=200, y=200)
elements.add(source="one", target="two", label="Node 1 to 2")

app = dash.Dash(__name__)
app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape',
        elements=elements.to_dash(),
        layout={'name': 'preset'}
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
```
Example2: Edit json file of Elements.
```python
from dash_cytoscape_elements import Elements

e = Elements.from_file("elements.json")
e.remove(id="node2")
e.remove(source="node1", target="node2")

with open("elements.json", mode='w') as f:
    f.write(e.to_json())
```

Please see the [Documentation](https://minefuto.github.io/dash-cytoscape-elements/) for details.
