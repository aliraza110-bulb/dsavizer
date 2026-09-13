import pytest

from data_structures.general_tree import GeneralTree


def test_general_tree_relationships_and_traversals() -> None:
    tree = GeneralTree[int]()
    tree.add_node(1)
    tree.add_node(2, 1)
    tree.add_node(3, 1)
    tree.add_node(4, 2)

    assert tree.preorder() == [1, 2, 4, 3]
    assert tree.postorder() == [4, 2, 3, 1]
    assert tree.level_order() == [1, 2, 3, 4]
    assert tree.inorder() == [4, 2, 3, 1]


def test_general_tree_delete_removes_subtree() -> None:
    tree = GeneralTree[int]()
    tree.add_node(1)
    tree.add_node(2, 1)
    tree.add_node(3, 2)

    tree.delete(2)

    assert tree.preorder() == [1]
    assert tree.find(3) is None


def test_general_tree_rejects_invalid_relationships() -> None:
    tree = GeneralTree[int]()
    tree.add_node(1)

    with pytest.raises(ValueError):
        tree.add_node(1)
    with pytest.raises(ValueError):
        tree.add_node(2, 99)
