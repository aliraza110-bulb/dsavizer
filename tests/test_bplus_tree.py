import pytest

from data_structures.bplus_tree import BPlusTree


def test_bplus_tree_search_and_leaf_traversal() -> None:
    tree = BPlusTree[int](order=4)
    for key in [30, 10, 50, 20, 40, 60, 70, 80]:
        tree.insert(key)

    assert tree.search(40)
    assert not tree.search(99)
    assert tree.leaf_traversal() == [10, 20, 30, 40, 50, 60, 70, 80]
    assert not tree.root.is_leaf


def test_bplus_tree_splits_and_rejects_duplicates() -> None:
    tree = BPlusTree[int](order=3)
    assert not tree.insert(10)
    assert not tree.insert(20)
    assert tree.insert(30)

    with pytest.raises(ValueError):
        tree.insert(20)


def test_bplus_tree_rejects_small_order_and_resets() -> None:
    with pytest.raises(ValueError):
        BPlusTree(order=2)
    tree = BPlusTree[int]()
    for key in [1, 2, 3]:
        tree.insert(key)
    tree.clear()
    assert tree.leaf_traversal() == []
