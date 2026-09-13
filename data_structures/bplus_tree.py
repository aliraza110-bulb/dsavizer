"""Small educational B+ tree with linked leaves."""

from bisect import bisect_left, bisect_right
from dataclasses import dataclass, field
from typing import Generic, TypeVar


Key = TypeVar("Key")


@dataclass
class BPlusNode(Generic[Key]):
    is_leaf: bool
    keys: list[Key] = field(default_factory=list)
    children: list["BPlusNode[Key]"] = field(default_factory=list)
    next_leaf: "BPlusNode[Key] | None" = None


class BPlusTree(Generic[Key]):
    """B+ tree whose order is the maximum number of children per internal node."""

    def __init__(self, order: int = 4) -> None:
        if order < 3:
            raise ValueError("B+ tree order must be at least 3.")
        self.order = order
        self.root = BPlusNode[Key](is_leaf=True)

    def insert(self, key: Key) -> bool:
        """Insert a unique key and return whether a split occurred."""
        split = self._insert(self.root, key)
        if split is None:
            return False
        promoted, right = split
        self.root = BPlusNode(
            is_leaf=False,
            keys=[promoted],
            children=[self.root, right],
        )
        return True

    def search(self, key: Key) -> bool:
        leaf = self._find_leaf(key)
        index = bisect_left(leaf.keys, key)
        return index < len(leaf.keys) and leaf.keys[index] == key

    def leaf_traversal(self) -> list[Key]:
        leaf = self.root
        while not leaf.is_leaf:
            leaf = leaf.children[0]
        result: list[Key] = []
        while leaf is not None:
            result.extend(leaf.keys)
            leaf = leaf.next_leaf
        return result

    def clear(self) -> None:
        self.root = BPlusNode[Key](is_leaf=True)

    def _find_leaf(self, key: Key) -> BPlusNode[Key]:
        node = self.root
        while not node.is_leaf:
            node = node.children[bisect_right(node.keys, key)]
        return node

    def _insert(
        self, node: BPlusNode[Key], key: Key
    ) -> tuple[Key, BPlusNode[Key]] | None:
        if node.is_leaf:
            position = bisect_left(node.keys, key)
            if position < len(node.keys) and node.keys[position] == key:
                raise ValueError(f"Key {key!r} already exists in the tree.")
            node.keys.insert(position, key)
            if len(node.keys) < self.order:
                return None
            midpoint = len(node.keys) // 2
            right = BPlusNode[Key](is_leaf=True, keys=node.keys[midpoint:])
            node.keys = node.keys[:midpoint]
            right.next_leaf = node.next_leaf
            node.next_leaf = right
            return right.keys[0], right

        child_index = bisect_right(node.keys, key)
        split = self._insert(node.children[child_index], key)
        if split is None:
            return None
        promoted, right = split
        node.keys.insert(child_index, promoted)
        node.children.insert(child_index + 1, right)
        if len(node.children) < self.order:
            return None
        midpoint = len(node.keys) // 2
        promoted = node.keys[midpoint]
        right_internal = BPlusNode[Key](
            is_leaf=False,
            keys=node.keys[midpoint + 1 :],
            children=node.children[midpoint + 1 :],
        )
        node.keys = node.keys[:midpoint]
        node.children = node.children[: midpoint + 1]
        return promoted, right_internal
