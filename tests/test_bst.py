import pytest

from data_structures.bst import BinarySearchTree


def test_bst_insert_search_and_traversals() -> None:
    tree = BinarySearchTree([50, 30, 70, 20, 40, 60, 80])

    assert tree.search(60)
    assert not tree.search(99)
    assert tree.inorder() == [20, 30, 40, 50, 60, 70, 80]
    assert tree.preorder() == [50, 30, 20, 40, 70, 60, 80]
    assert tree.postorder() == [20, 40, 30, 60, 80, 70, 50]
    assert tree.level_order() == [50, 30, 70, 20, 40, 60, 80]


def test_bst_delete_handles_leaf_one_child_and_two_children() -> None:
    tree = BinarySearchTree([50, 30, 70, 20, 40, 60, 80])

    tree.delete(20)
    tree.delete(30)
    tree.delete(50)

    assert tree.inorder() == [40, 60, 70, 80]
    assert tree.minimum() == 40
    assert tree.maximum() == 80


def test_bst_rejects_duplicates_and_missing_values() -> None:
    tree = BinarySearchTree[int]()
    tree.insert(10)

    with pytest.raises(ValueError):
        tree.insert(10)
    with pytest.raises(KeyError):
        tree.delete(99)
