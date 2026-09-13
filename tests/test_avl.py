import pytest

from data_structures.avl import AVLTree, AVLNode


def assert_balanced(node: AVLNode[int] | None) -> int:
    if node is None:
        return 0
    left_height = assert_balanced(node.left)
    right_height = assert_balanced(node.right)
    assert abs(left_height - right_height) <= 1
    assert node.height == 1 + max(left_height, right_height)
    return node.height


@pytest.mark.parametrize(
    ("values", "rotation", "root_value"),
    [
        ([30, 20, 10], "LL", 20),
        ([10, 20, 30], "RR", 20),
        ([30, 10, 20], "LR", 20),
        ([10, 30, 20], "RL", 20),
    ],
)
def test_avl_performs_all_rotation_types(
    values: list[int], rotation: str, root_value: int
) -> None:
    tree = AVLTree[int]()
    for value in values:
        last_rotation = tree.insert(value)

    assert last_rotation == rotation
    assert tree.root is not None
    assert tree.root.value == root_value
    assert tree.inorder() == sorted(values)
    assert_balanced(tree.root)


def test_avl_delete_preserves_balance() -> None:
    tree = AVLTree([50, 30, 70, 20, 40, 60, 80, 10])

    tree.delete(80)
    tree.delete(50)

    assert tree.inorder() == [10, 20, 30, 40, 60, 70]
    assert_balanced(tree.root)
    assert tree.height() == 3


def test_avl_rejects_duplicates_and_missing_values() -> None:
    tree = AVLTree[int]()
    tree.insert(10)

    with pytest.raises(ValueError):
        tree.insert(10)
    with pytest.raises(KeyError):
        tree.delete(99)
