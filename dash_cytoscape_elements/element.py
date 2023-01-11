"""The data structures of Dash Cystoscape/Cytoscape.js element."""
from typing import Any, Dict, List, Set

from pydantic import BaseModel, Field, validator

__all__ = ["Edge", "EdgeData", "Node", "NodeData", "Position"]


class BaseElement(BaseModel):
    class Config:
        validate_assignment: bool = True
        allow_population_by_field_name: bool = True
        extra: str = "forbid"

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
            return False

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
    def is_match(self, **kwargs: Any) -> bool:
        for k, v in kwargs.items():
            if k == "classes":
                return set(self.classes.split()) >= set(v.split())
            if not (self.is_match_attribute(k, v)):
                return False
        return True

    def _add_classes(self, value: str):
        classes = self.classes.split()
        for c in value.split():
            if not (c in classes):
                classes.append(c)
        self.classes = " ".join([c for c in classes])

    def add(self, **kwargs: Any):
        for k, v in kwargs.items():
            if k == "classes":
                self._add_classes(v)
            else:
                self.add_attribute(k, v)


class Node(Element):

    group: str = ""
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

    def __str__(self) -> str:
        return 'Node(id="{}")'.format(self.data.id)


class Edge(Element):

    group: str = ""
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

    def __str__(self) -> str:
        return 'Edge(id="{}")'.format(self.data.id)
