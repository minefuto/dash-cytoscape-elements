import pytest

from dash_cytoscape_elements import Elements
from dash_cytoscape_elements.element import Edge, Node


@pytest.fixture
def init():
    elements = Elements.from_file("./tests/mock_data/init.json")
    return elements


@pytest.fixture
def conversion():
    elements = Elements.from_file("./tests/mock_data/conversion.json")
    return elements


def test_filter_success(init):
    filter = init.filter(group="nodes")
    assert filter == Elements.from_file("./tests/mock_data/filter_success.json")

    filter_classes = init.filter(classes="node3.1")
    assert filter_classes == Elements.from_file(
        "./tests/mock_data/filter_success_classes.json"
    )


def test_filter_failed(init):
    filter = init.filter(group="nodes", id="edge1")
    assert filter == Elements()


def test_get_node_success(init):
    node = init.get(id="node1")
    assert node == Node.parse_file("./tests/mock_data/get_node_success.json")


def test_get_node_fail(init):
    node = init.get(id="node4")
    assert node is None


def test_get_edge_success(init):
    edge = init.get(source="node1", target="node2")
    assert edge == Edge.parse_file("./tests/mock_data/get_edge_success.json")


def test_get_edge_fail(init):
    edge = init.get(id="edge1")
    assert edge is None


def test_add_node_success(init):
    init.add(
        id="node5",
        parent="node5_parent",
        label="node5_label",
        x=1.0,
        y=1.0,
        selected=True,
        selectable=False,
        locked=True,
        grabbable=False,
        pannable=True,
        classes="node1 node2 node3",
        scratch={"scratch1_key": "scratch1_value", "scratch2_key": "scratch2_value"},
    )
    init.add(
        id="node1",
        parent="node1_parent2",
        label="node5_label2",
        x=1.0,
        y=1.0,
        selected=True,
        selectable=False,
        locked=True,
        grabbable=False,
        pannable=True,
        classes="node1 node2 node3",
        scratch={"scratch1_key": "scratch1_value", "scratch2_key": "scratch2_value"},
    )
    assert init == Elements.from_file("./tests/mock_data/add_node_success.json")


def test_add_node_fail(init):
    init.add(id="node1", no_data="no_data")
    init.add(id="node1", group="edges")
    assert init == Elements.from_file("./tests/mock_data/init.json")


def test_add_edge_success(init):
    init.add(
        id="edge4",
        source="node3",
        target="node2",
        label="edge4_label",
        source_label="node3_label",
        target_label="node2_label",
        selected=True,
        selectable=False,
        locked=True,
        grabbable=False,
        pannable=False,
        classes="edge1 edge2 edge3",
        scratch={"scratch1_key": "scratch1_value", "scratch2_key": "scratch2_value"},
    )
    init.add(
        id="edge1.1",
        source="node1",
        target="node2",
        label="edge1.1_label",
        source_label="node1_label2",
        target_label="node2_label2",
        selected=True,
        selectable=False,
        locked=True,
        grabbable=False,
        pannable=False,
        classes="edge1.1",
        scratch={"scratch1_key": "scratch1_value", "scratch2_key": "scratch2_value"},
    )
    assert init == Elements.from_file("./tests/mock_data/add_edge_success.json")


def test_add_edge_fail(init):
    init.add(parent="edge1", source="node1", target="node3")
    init.add(id="edge1", source="node1", target="node3")
    init.add(id="edge1", group="nodes")
    assert init == Elements.from_file("./tests/mock_data/init.json")


def test_remove_node_success(init):
    init.remove(id="node2")
    assert init == Elements.from_file("./tests/mock_data/remove_node_success.json")


def test_remove_node_fail(init):
    init.remove(id="node4")
    init.remove(parent="node1_parent")
    assert init == Elements.from_file("./tests/mock_data/init.json")


def test_remove_edge_success(init):
    init.remove(source="node1", target="node3")
    assert init == Elements.from_file("./tests/mock_data/remove_edge_success.json")


def test_remove_edge_fail(init):
    init.remove(source="node3", target="node1")
    init.remove(source="node1")
    assert init == Elements.from_file("./tests/mock_data/init.json")


def test_to_json(conversion):
    assert Elements.from_json(conversion.to_json()) == conversion


def test_to_dash(conversion):
    assert Elements.from_dash(conversion.to_dash()) == conversion
