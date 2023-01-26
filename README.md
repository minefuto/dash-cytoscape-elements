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
### Example1
Create Elements object & using on Dash Cytoscape  
```python
import dash
import dash_cytoscape as cyto
from dash import html
from dash_cytoscape_elements import Elements

e = Elements()
e.add(id="one", label="Node 1", x=50, y=50)
e.add(id="two", label="Node 2", x=200, y=200)
e.add(source="one", target="two", label="Node 1 to 2")

app = dash.Dash(__name__)
app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape',
        elements=e.to_dash(),
        layout={'name': 'preset'}
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
```
### Example2
Edit json file of Elements.
```python
from dash_cytoscape_elements import Elements

e = Elements.from_file("elements.json")
e.remove(id="node2")
e.remove(source="node1", target="node2")

with open("elements.json", mode='w') as f:
    f.write(e.to_json())
```
### Supported Parameters
This package supports the following parameters of [Dash Cytoscape](https://github.com/plotly/dash-cytoscape) Element.  

| Parameter | Type | Element |
| --------- | ---- | ------- |
| id |  str | Node, Edge |
| parent | str | Node |
| source | str | Edge |
| target | str | Edge |
| label | str | Node, Edge |
| source_label | str | Edge |
| target_label | str | Edge |
| x | float | Node |
| y | float | Node |
| classes | str | Node, Edge |
| selected | str | Node, Edge |
| selectable | str | Node, Edge |
| locked | str | Node, Edge |
| grabbable | str | Node, Edge |
| pannable | str | Node, Edge |
| scratch | dict | Node, Edge |

example output:
```python
>>> e = Elements()
>>> e.add(id="node1", parent="parent1", label="node_label1", x=1, y=1, classes="class1")
>>> e.add(source="node1", target="node2", label="edge_label1", source_label="source_label1", target_label="target_label1", classes="class1")
>>> print(e.to_json())
[
    {
        "group": "nodes",
        "classes": "class1",
        "data": {
            "id": "node1",
            "parent": "parent1",
            "label": "node_label1"
        },
        "position": {
            "x": 1.0,
            "y": 1.0
        }
    },
    {
        "group": "edges",
        "classes": "class1",
        "data": {
            "id": "49082bcd-dcbb-4db7-b369-29e3bf8f74e2",
            "source": "node1",
            "target": "node2",
            "label": "edge_label1",
            "source-label": "source_label1",
            "target-label": "target_label1"
        }
    }
]
```
How to add your own parameters:
```python
from typing import List, Set
from dash_cytoscape_elements import GenericElements
from dash_cytoscape_elements.element import Edge, EdgeData, Node, NodeData


class CustomNodeData(NodeData):
    custom_str1: str = ""

class CustomNode(Node):
    data: CustomNodeData = CustomNodeData()
    custom_str2: str = ""
    custom_list: List[str] = []

class CustomEdgeData(EdgeData):
    custom_str1: str = ""

class CustomEdge(Edge):
    data: CustomEdgeData = CustomEdgeData()
    custom_str2: str = ""
    custom_set: Set[str] = set()

e = GenericElements[CustomNode, CustomEdge]()
e.add(id="node1", custom_str1="str1", custom_str2="str2", custom_list=["list1", "list2"])
e.add(id="edge1", source="node1", target="node2", custom_str1="str1", custom_str2="str2", custom_set={"set1", "set2"})

print(e.to_json())
# [
#     {
#         "group": "nodes",
#         "data": {
#             "id": "node1",
#             "custom_str1": "str1"
#         },
#         "custom_str2": "str2",
#         "custom_list": [
#             "list1",
#             "list2"
#         ]
#     },
#     {
#         "group": "edges",
#         "data": {
#             "id": "edge1",
#             "source": "node1",
#             "target": "node2",
#             "custom_str1": "str1"
#         },
#         "custom_str2": "str2",
#         "custom_set": [
#             "set1",
#             "set2"
#         ]
#     }
# ]
```

Please see the [Documentation](https://minefuto.github.io/dash-cytoscape-elements/) for details.
