"""The main module of this package."""
import uuid
from typing import Any, ClassVar, ForwardRef, List, Optional, Set, Union

from pydantic import BaseModel

from .element import Edge, Element, Node

Elements = ForwardRef("Elements")


class Elements(BaseModel):
    """This class is a List of Element(Node/Edge) object."""

    node: ClassVar[Node] = Node
    """The Node class to be stored in the Elements."""
    node_keys: ClassVar[Set[str]] = {"id"}
    """The parameters that uniquely identify the specific Node object in the Elements.

    default is `{ "id" }`
    """
    edge: ClassVar[Edge] = Edge
    """The Edge class to be stored in the Elements."""
    edge_keys: ClassVar[Set[str]] = {"source", "target"}
    """The parameters that uniquely identify the specific Edge object in the Elements.

    default is `{ "source", "target" }`
    """

    __root__: List[Union[node, edge]] = []

    def __str__(self) -> str:
        return "[{}]".format(", ".join([str(e) for e in self.__root__]))

    def __iter__(self):
        return iter(self.__root__)

    def _append(self, element: Element):
        self.__root__.append(element)

    def _remove(self, element: Element):
        self.__root__.remove(element)

    @classmethod
    def from_dash(cls, data: List) -> Elements:
        """Create the Elements from the element object of Dash Cytoscape format.

        Args:
            data (List): no comment

        Returns:
            Elements: no comment

        Notes:
            * [Dash Cytoscape format](https://dash.plotly.com/cytoscape/reference)
        """
        return cls.parse_obj(data)

    @classmethod
    def from_file(cls, path: str) -> Elements:
        """Create the Elements from the json file of Cytoscape.js format.

        Args:
            path (str): no comment

        Returns:
            Elements: no comment

        Notes:
            * [Cytoscape.js format](https://js.cytoscape.org/#notation/elements-json)
        """
        return cls.parse_file(path)

    @classmethod
    def from_json(cls, data: str) -> Elements:
        """Create the Elements from the json string of Cytoscape.js format.

        Args:
            data (str): no comment

        Returns:
            Elements: no comment

        Notes:
            * [Cytoscape.js format](https://js.cytoscape.org/#notation/elements-json)
        """
        return cls.parse_raw(data)

    def to_dash(self) -> List:
        """Create the element object of Dash Cytoscape format.

        Returns:
            List: no comment

        Notes:
            * [Dash Cytoscape format](https://dash.plotly.com/cytoscape/reference)
        """
        elements_dict = self.dict(exclude_defaults=True, by_alias=True)
        if elements_dict:
            return elements_dict["__root__"]
        return []

    def to_json(self) -> str:
        """Create the json raw string of Cytoscape.js format.

        Returns:
            str: no comment

        Notes:
            * [Cytoscape.js format](https://js.cytoscape.org/#notation/elements-json)
        """
        if self.__root__:
            return self.json(exclude_defaults=True, indent=4, by_alias=True)
        return ""

    def filter(self, **kwargs: Any) -> Elements:
        """Get the Elements contains Element(Node/Edge) objects that match kwargs.

        Args:
            **kwargs (Any): no comment

        Returns:
            Elements: no comment

        Examples:
            >>> e = Elements()
            >>> e.add(id="node1", parent="p1", classes="test test2")
            >>> e.add(id="node2", parent="p1")
            >>> e.add(id="edge1", source="node1", target="node2")
            >>> e.add(id="edge2", source="node2", target="node1", classes="test")
            >>>
            >>> print(e)
            [Node(id="node1"), Node(id="node2"), Edge(id="edge1"), Edge(id="edge2")]
            >>> print(e.filter(classes="test"))
            [Node(id="node1"), Edge(id="edge2")]
            >>> print(e.filter(parent="p1"))
            [Node(id="node1"), Node(id="node2")]

        Note:
            * Match criteria of filter
                * List/Dict/Set and `classes`: include value or not
                * The others Type: exact match value or not
        """
        elements = Elements()
        for e in self:
            if e.is_match(**kwargs):
                elements._append(e)
        return elements

    def get(self, **kwargs: Any) -> Optional[Element]:
        """Get the Element(Node/Edge) object in the Elements matching the `kwargs`.

        Must specify the values that uniquely identify the Element in the `kwargs`.
        The others parameters are ignored.

        Args:
            **kwargs (Any): the values of `Elements.node_keys` or `Elements.edge_keys`

        Returns:
            Optional[Element]:

        Examples:
            >>> e = Elements()
            >>> e.add(id="node1")
            >>> e.add(id="node2")
            >>> e.add(id="edge1", source="node1", target="node2")
            >>> e.add(id="edge2", source="node2", target="node1")
            >>> print(e)
            [Node(id="node1"), Node(id="node2"), Edge(id="edge1"), Edge(id="edge2")]
            >>>
            >>> print(e.get(id="node1"))
            Node(id="node1")
            >>>
            >>> print(e.get(source="node1", target="node2"))
            Edge(id="edge1")
            >>>
            >>> print(e.get(id="node3"))
            None
        """
        if kwargs.keys() >= self.node_keys:
            key_dict = {k: kwargs[k] for k in self.node_keys}
            for e in self.filter(group="nodes"):
                if e.is_match(**key_dict):
                    return e

        if kwargs.keys() >= self.edge_keys:
            key_dict = {k: kwargs[k] for k in self.edge_keys}
            for e in self.filter(group="edges"):
                if e.is_match(**key_dict):
                    return e

        return None

    def add(self, **kwargs: Any):
        """Add the Element(Node/Edge) object to the Elements.

        If exist `source` and `edge` in `kwargs`, add the Edge Element.
        Otherwise add the Node Element.

        Args:
            **kwargs (Any): each class variables in `dash_cytoscape_elements.element`

        Returns:
            Optional[Element]:

        Examples:
            >>> e = Elements()
            >>> e.add(id="node1", classes="test", label="node1_label")
            >>> pprint(e.to_dash())
            [{'classes': 'test',
              'data': {'id': 'node1', 'label': 'node1_label'},
              'group': 'nodes'}]
            >>> e.add(source="node1", target="node2")
            >>> pprint(e.to_dash())
            [{'classes': 'test',
              'data': {'id': 'node1', 'label': 'node1_label'},
              'group': 'nodes'},
             {'data': {'id': 'dd2f9795-aa91-4532-9a00-438ad454799b',
                       'source': 'node1',
                       'target': 'node2'},
              'group': 'edges'}]
            >>> e.add(id="node1", classes="test2", label="node1.2")
            >>> e.add(source="node1", target="node2", label="edge1")
            >>> pprint(e.to_dash())
            [{'classes': 'test test2',
              'data': {'id': 'node1', 'label': 'node1.2'},
              'group': 'nodes'},
             {'data': {'id': 'dd2f9795-aa91-4532-9a00-438ad454799b',
                       'label': 'edge1',
                       'source': 'node1',
                       'target': 'node2'},
              'group': 'edges'}]

        Note:
            * UUID is assigned if not exist `id` in the `kwargs`.
            * If already exist Element, update the Element(Node/Edge) parameters.
                * List/Dict/Set and `classes`: append value
                * The others Type: replace value
        """
        element = self.get(**kwargs)

        if element:
            if "id" in kwargs:
                for e in self.filter(id=kwargs["id"]):
                    if e != element:
                        return
            element.add(**kwargs)
            return

        if "source" in kwargs and "target" in kwargs:
            element = self.edge()
        else:
            element = self.node()

        if "id" in kwargs:
            if self.filter(id=kwargs["id"]).__root__:
                return
            element.add(**kwargs)
        else:
            element.add(**kwargs, id=str(uuid.uuid4()))

        self._append(element)

    def remove(self, **kwargs: Any):
        """Remove the Element(Node/Edge) object in the Elements.

        Must specify the values that uniquely identify the Element in the `kwargs`.
        The others parameters are ignored.

        Args:
            **kwargs (Any): the values of `Elements.node_keys` or `Elements.edge_keys`

        Examples:
            >>> e = Elements()
            >>> e.add(id="node1")
            >>> e.add(id="node2")
            >>> e.add(id="edge1", source="node1", target="node2")
            >>> e.add(id="edge2", source="node2", target="node1")
            >>> print(e)
            [Node(id="node1"), Node(id="node2"), Edge(id="edge1"), Edge(id="edge2")]
            >>>
            >>> e.remove(id="node1")
            >>> print(e)
            [Node(id="node2"), Edge(id="edge1"), Edge(id="edge2")]
            >>>
            >>> e.remove(id="node3")
            >>> print(e)
            [Node(id="node2"), Edge(id="edge1"), Edge(id="edge2")]
        """
        element = self.get(**kwargs)
        if element:
            self._remove(element)


Elements.update_forward_refs()
