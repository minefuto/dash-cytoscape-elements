"""The main module of this package."""
import uuid
from typing import Any, ClassVar, Generic, List, Set, Tuple, Type, TypeVar, Union

from pydantic.generics import GenericModel, GenericModelT
from typing_extensions import TypeAlias

from .element import Edge, Node

NodeT = TypeVar("NodeT", bound=Node)
EdgeT = TypeVar("EdgeT", bound=Edge)


class GenericElements(GenericModel, Generic[NodeT, EdgeT]):
    """This generic class is a List of Element(`element.Node`/`element.Edge`) object.

    It can specify the type of Element(`element.Node`/`element.Edge`).

    Basically to use Elements(Type Alias of `Elements`).
    """

    node_keys: ClassVar[Set[str]] = {"id"}
    """The parameters that uniquely identify the specific Node object
    in the `GenericElements`.

    default is `{ "id" }`
    """

    edge_keys: ClassVar[Set[str]] = {"source", "target"}
    """The parameters that uniquely identify the specific Edge object
    in the `GenericElements`.

    default is `{ "source", "target" }`
    """

    __NodeType__: ClassVar[Type[Any]]
    __EdgeType__: ClassVar[Type[Any]]
    __root__: List[Union[NodeT, EdgeT]] = []

    def __class_getitem__(  # type: ignore[override]
        cls: Type[GenericModelT], params: Tuple[Type[Node], Type[Edge]]
    ) -> Type[Any]:
        model = super().__class_getitem__(params)
        model.__NodeType__, model.__EdgeType__ = params
        return model

    def __str__(self) -> str:
        return "[{}]".format(", ".join([str(e) for e in self.__root__]))

    def __iter__(self):
        return iter(self.__root__)

    def _append(self, element: Union[NodeT, EdgeT]) -> None:
        self.__root__.append(element)

    def _remove(self, element: Union[NodeT, EdgeT]) -> None:
        self.__root__.remove(element)

    @classmethod
    def from_dash(cls, data: List) -> "GenericElements":
        """Create the `GenericElements` from the element object of Dash Cytoscape format.

        Args:
            data (List): no comment

        Returns:
            GenericElements: no comment

        Notes:
            * [Dash Cytoscape format](https://dash.plotly.com/cytoscape/reference)
        """
        return cls.parse_obj(data)

    @classmethod
    def from_file(cls, path: str) -> "GenericElements":
        """Create the `GenericElements` from the json file of Cytoscape.js format.

        Args:
            path (str): no comment

        Returns:
            GenericElements: no comment

        Notes:
            * [Cytoscape.js format](https://js.cytoscape.org/#notation/elements-json)
        """
        return cls.parse_file(path)

    @classmethod
    def from_json(cls, data: str) -> "GenericElements":
        """Create the `GenericElements` from the json string of Cytoscape.js format.

        Args:
            data (str): no comment

        Returns:
            GenericElements: no comment

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

    def filter(self, **kwargs: Any) -> "GenericElements":
        """Get the `GenericElements` contains Element(`element.Node`/`element.Edge`)
         objects that match `kwargs`.

        Args:
            **kwargs (Any): no comment

        Returns:
            GenericElements: no comment

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

    def get(self, **kwargs: Any) -> Union[NodeT, EdgeT, None]:
        """Get the Element(`element.Node`/`element.Edge`) object
         in the `GenericElements` matching the `kwargs`.

        Must specify the values that uniquely identify the Element in the `kwargs`.
        The others parameters are ignored.

        Args:
            **kwargs (Any): the values of `GenericElements.node_keys`
             or `GenericElements.edge_keys`

        Returns:
            Union[element.Node, element.Edge, None]: no comment

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

    def add(self, **kwargs: Any) -> None:
        """Add the Element(`element.Node`/`element.Edge`) object to the `GenericElements`.

        If exist `source` and `target` in `kwargs`, add the `element.Edge`.
        Otherwise add the `element.Node`.

        Args:
            **kwargs (Any): each class variables in `element`

        Returns:
            None: no comment

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
            * If already exist Element, update the Element(`element.Node`/`element.Edge`) parameters.
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

        new_element: Union[NodeT, EdgeT] = (
            self.__EdgeType__()
            if "source" in kwargs and "target" in kwargs
            else self.__NodeType__()
        )
        if "id" in kwargs:
            if self.filter(id=kwargs["id"]).__root__:
                return
            new_element.add(**kwargs)
        else:
            new_element.add(**kwargs, id=str(uuid.uuid4()))

        self._append(new_element)

    def remove(self, **kwargs: Any) -> None:
        """Remove the Element(`element.Node`/`element.Edge`) object in the `GenericElements`.

        Must specify the values that uniquely identify the Element in the `kwargs`.
        The others parameters are ignored.

        Args:
            **kwargs (Any): the values of `GenericElements.node_keys`
             or `GenericElements.edge_keys`

        Returns:
            None: no comment

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


Elements: TypeAlias = GenericElements[Node, Edge]
