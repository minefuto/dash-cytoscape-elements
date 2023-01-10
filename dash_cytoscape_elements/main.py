import uuid
from typing import Any, ClassVar, Dict, ForwardRef, List, Optional, Set, Union

from pydantic import BaseModel, Field, validator

Elements = ForwardRef("Elements")


class BaseElement(BaseModel):
    class Config:
        validate_assignment = True
        allow_population_by_field_name = True
        extra = "forbid"

    def is_match_attribute(self, key: str, value: Any) -> bool:
        if hasattr(self, key):
            if isinstance(getattr(self, key), List):
                if isinstance(value, List):
                    return set(getattr(self, key)) >= set(value)
                else:
                    return value in getattr(self, key)
            elif isinstance(getattr(self, key), Set):
                if isinstance(value, Set):
                    return getattr(self, key) >= value
                else:
                    return value in getattr(self, key)
            elif isinstance(getattr(self, key), Dict):
                for k, v in value.items():
                    if getattr(self, key)[k] != v:
                        return False
                return True
            else:
                return getattr(self, key) == value
        else:
            for v in self.__dict__.values():
                if isinstance(v, BaseElement):
                    return v.is_match_attribute(key, value)

    def add_attribute(self, key: str, value: Any):
        if hasattr(self, key):
            if isinstance(getattr(self, key), List):
                if isinstance(value, List):
                    for v in value:
                        if not (v in getattr(self, key)):
                            getattr(self, key).append(v)
                else:
                    if not (value in getattr(self, key)):
                        getattr(self, key).append(value)
            if isinstance(getattr(self, key), Set):
                if isinstance(value, Set):
                    for v in value:
                        if not (v in getattr(self, key)):
                            getattr(self, key).add(v)
                else:
                    if not (value in getattr(self, key)):
                        getattr(self, key).append(value)
            elif isinstance(getattr(self, key), Dict):
                for k, v in value.items():
                    getattr(self, key)[k] = v
            else:
                setattr(self, key, value)
        else:
            for v in self.__dict__.values():
                if isinstance(v, BaseElement):
                    v.add_attribute(key, value)


class Position(BaseElement):
    x: float = 0.0
    y: float = 0.0


class NodeData(BaseElement):
    id: str = ""
    parent: str = ""
    label: str = ""


class EdgeData(BaseElement):
    id: str = ""
    source: str = ""
    target: str = ""
    label: str = ""
    source_label: str = Field(default="", alias="source-label")
    target_label: str = Field(default="", alias="target-label")


class Element(BaseElement):
    def is_match(self, **kwargs) -> bool:
        for k, v in kwargs.items():
            if k == "classes":
                return set(self.classes.split()) >= set(v.split())
            if not (self.is_match_attribute(k, v)):
                return False
        return True

    def _add_classes(self, value):
        classes = self.classes.split()
        for c in value.split():
            if not (c in classes):
                if self.classes:
                    self.classes = self.classes + " {}".format(c)
                else:
                    self.classes = c

    def add(self, **kwargs):
        for k, v in kwargs.items():
            if k == "classes":
                self._add_classes(v)
            else:
                self.add_attribute(k, v)


class Node(Element):
    keys: ClassVar[Set[str]] = {"id"}

    group: str = "nodes"
    data: NodeData = NodeData()
    position: Position = Position()
    selected: bool = False
    selectable: bool = True
    locked: bool = False
    grabbable: bool = True
    pannable: bool = False
    classes: str = ""
    scratch: Dict = {}

    @validator("group", always=True)
    def generate_group(cls, group):
        if group != "nodes":
            return "nodes"
        return group


class Edge(Element):
    keys: ClassVar[Set[str]] = {"source", "target"}

    group: str = "edges"
    data: EdgeData = EdgeData()
    selected: bool = False
    selectable: bool = True
    locked: bool = False
    grabbable: bool = True
    pannable: bool = True
    classes: str = ""
    scratch: Dict = {}

    @validator("group", always=True)
    def generate_group(cls, group):
        if group != "edges":
            return "edges"
        return group


class Elements(BaseModel):
    node: ClassVar[Node] = Node
    edge: ClassVar[Edge] = Edge

    __root__: List[Union[node, edge]] = []

    def __iter__(self):
        return iter(self.__root__)

    def _append(self, element):
        self.__root__.append(element)

    def _remove(self, element):
        self.__root__.remove(element)

    def to_json(self) -> str:
        if self.__root__:
            return self.json(exclude_defaults=True, indent=4, by_alias=True)
        return ""

    def to_dict(self) -> List:
        elements_dict = self.dict(exclude_defaults=True, by_alias=True)
        if elements_dict:
            return elements_dict["__root__"]
        return []

    def filter(self, **kwargs) -> Elements:
        elements = Elements()
        for e in self:
            if e.is_match(**kwargs):
                elements._append(e)
        return elements

    def get(self, **kwargs) -> Optional[Element]:
        if kwargs.keys() >= self.node.keys:
            key_dict = {k: kwargs[k] for k in self.node.keys}
            for e in self.filter(group="nodes"):
                if e.is_match(**key_dict):
                    return e

        if kwargs.keys() >= self.edge.keys:
            key_dict = {k: kwargs[k] for k in self.edge.keys}
            for e in self.filter(group="edges"):
                if e.is_match(**key_dict):
                    return e

        return None

    def add(self, **kwargs):
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

    def remove(self, **kwargs):
        element = self.get(**kwargs)
        if element:
            self._remove(element)


Elements.update_forward_refs()
