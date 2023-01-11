import uuid
from typing import Any, ClassVar, ForwardRef, List, Optional, Set, Union

from pydantic import BaseModel

from .element import Edge, Element, Node

Elements = ForwardRef("Elements")


class Elements(BaseModel):
    node: ClassVar[Node] = Node
    node_keys: ClassVar[Set[str]] = {"id"}
    edge: ClassVar[Edge] = Edge
    edge_keys: ClassVar[Set[str]] = {"source", "target"}

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
        return cls.parse_obj(data)

    @classmethod
    def from_file(cls, path: str) -> Elements:
        return cls.parse_file(path)

    @classmethod
    def from_json(cls, data: str) -> Elements:
        return cls.parse_raw(data)

    def to_dash(self) -> List:
        elements_dict = self.dict(exclude_defaults=True, by_alias=True)
        if elements_dict:
            return elements_dict["__root__"]
        return []

    def to_json(self) -> str:
        if self.__root__:
            return self.json(exclude_defaults=True, indent=4, by_alias=True)
        return ""

    def filter(self, **kwargs: Any) -> Elements:
        elements = Elements()
        for e in self:
            if e.is_match(**kwargs):
                elements._append(e)
        return elements

    def get(self, **kwargs: Any) -> Optional[Element]:
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
        element = self.get(**kwargs)
        if element:
            self._remove(element)


Elements.update_forward_refs()
