"""Test for node ID increment functionality."""

from copy import deepcopy
import pytest
from dace.sdfg.nodes import Node, AccessNode, reset_node_id_counter


def test_node_id_increment():
    """Test that creating new nodes increments the ID."""
    with reset_node_id_counter():
        node1 = Node()
        node2 = Node()
        node3 = Node()

        # IDs should be unique and increasing
        assert node1.id == 0, "First node should have ID 0"
        assert node2.id == 1, "Second node should have ID 1"
        assert node3.id == 2, "Third node should have ID 2"


def test_node_deepcopy():
    """Test that deepcopy assigns a new ID."""
    with reset_node_id_counter():
        node1 = Node()
        node1_copy = deepcopy(node1)

        # Copied node should have a different ID
        assert node1.id == 0, "Original node should have ID 0"
        assert node1_copy.id == 1, "Copied node should have ID 1"
        assert node1_copy.id != node1.id, "Deepcopied node should have a different ID"
        assert node1_copy.guid != node1.guid, "Deepcopied node should have a different GUID"


def test_access_node_id():
    """Test that AccessNode also gets incremented IDs."""
    with reset_node_id_counter():
        access1 = AccessNode("data1")
        access2 = AccessNode("data2")

        # AccessNode IDs should be unique and increasing
        assert access1.id == 0, "First AccessNode should have ID 0"
        assert access2.id == 1, "Second AccessNode should have ID 1"


def test_access_node_deepcopy():
    """Test that deepcopy of AccessNode assigns a new ID."""
    with reset_node_id_counter():
        access1 = AccessNode("data1")
        access1_copy = deepcopy(access1)

        # Copied AccessNode should have a different ID
        assert access1.id == 0, "Original AccessNode should have ID 0"
        assert access1_copy.id == 1, "Copied AccessNode should have ID 1"
        assert access1_copy.id != access1.id, "Deepcopied AccessNode should have a different ID"
        assert access1_copy.guid != access1.guid, "Deepcopied AccessNode should have a different GUID"


def test_multiple_nodes_unique_ids():
    """Test that multiple nodes have unique IDs."""
    with reset_node_id_counter():
        nodes = [Node() for _ in range(10)]
        ids = [node.id for node in nodes]

        # All IDs should be unique
        assert len(ids) == len(set(ids)), "All node IDs should be unique"
        assert ids == list(range(10)), "IDs should be sequential from 0 to 9"


def test_context_manager_restores_counter():
    """Test that the context manager restores the old counter value."""
    with reset_node_id_counter():
        node1 = Node()
        assert node1.id == 0

    # Create a node outside the context manager
    node2 = Node()

    # Now use the context manager again
    with reset_node_id_counter():
        node3 = Node()
        assert node3.id == 0, "Counter should be reset to 0"

    # Create another node outside
    node4 = Node()
    # node4 should continue from where node2 left off
    assert node4.id == node2.id + 1, "Counter should be restored after context manager exits"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
