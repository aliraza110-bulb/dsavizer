"""Binary search tree implementation."""

from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Generic, TypeVar


Value = TypeVar("Value")


@dataclass
class BSTNode(Generic[Value]):
    value: Value
    left: "BSTNode[Value] | None" = None
    right: "BSTNode[Value] | None" = None


class BinarySearchTree(Generic[Value]):
    """Unbalanced BST with unique values."""

    def __init__(self, values: Iterable[Value] | None = None) -> None:
        self.root: BSTNode[Value] | None = None
        for value in values or []:
            self.insert(value)

    def insert(self, value: Value) -> None:
        self.root = self._insert(self.root, value)

    def search(self, value: Value) -> bool:
        current = self.root
        while current is not None:
            if value == current.value:
                return True
            current = current.left if value < current.value else current.right
        return False

    def delete(self, value: Value) -> None:
        self.root, deleted = self._delete(self.root, value)
        if not deleted:
            raise KeyError(f"Value {value!r} was not found.")

    def minimum(self) -> Value:
        if self.root is None:
            raise IndexError("Cannot find a minimum in an empty tree.")
        return self._minimum_node(self.root).value

    def maximum(self) -> Value:
        if self.root is None:
            raise IndexError("Cannot find a maximum in an empty tree.")
        current = self.root
        while current.right is not None:
            current = current.right
        return current.value

    def inorder(self) -> list[Value]:
        result: list[Value] = []
        self._inorder(self.root, result)
        return result

    def preorder(self) -> list[Value]:
        result: list[Value] = []
        self._preorder(self.root, result)
        return result

    def postorder(self) -> list[Value]:
        result: list[Value] = []
        self._postorder(self.root, result)
        return result

    def level_order(self) -> list[Value]:
        if self.root is None:
            return []
        result: list[Value] = []
        pending: deque[BSTNode[Value]] = deque([self.root])
        while pending:
            node = pending.popleft()
            result.append(node.value)
            if node.left is not None:
                pending.append(node.left)
            if node.right is not None:
                pending.append(node.right)
        return result

    def clear(self) -> None:
        self.root = None

    def _insert(self, node: BSTNode[Value] | None, value: Value) -> BSTNode[Value]:
        if node is None:
            return BSTNode(value)
        if value == node.value:
            raise ValueError(f"Value {value!r} already exists in the tree.")
        if value < node.value:
            node.left = self._insert(node.left, value)
        else:
            node.right = self._insert(node.right, value)
        return node

    def _delete(
        self, node: BSTNode[Value] | None, value: Value
    ) -> tuple[BSTNode[Value] | None, bool]:
        if node is None:
            return None, False
        if value < node.value:
            node.left, deleted = self._delete(node.left, value)
            return node, deleted
        if value > node.value:
            node.right, deleted = self._delete(node.right, value)
            return node, deleted
        if node.left is None:
            return node.right, True
        if node.right is None:
            return node.left, True
        successor = self._minimum_node(node.right)
        node.value = successor.value
        node.right, _ = self._delete(node.right, successor.value)
        return node, True

    @staticmethod
    def _minimum_node(node: BSTNode[Value]) -> BSTNode[Value]:
        while node.left is not None:
            node = node.left
        return node

    def _inorder(self, node: BSTNode[Value] | None, result: list[Value]) -> None:
        if node is not None:
            self._inorder(node.left, result)
            result.append(node.value)
            self._inorder(node.right, result)

    def _preorder(self, node: BSTNode[Value] | None, result: list[Value]) -> None:
        if node is not None:
            result.append(node.value)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def _postorder(self, node: BSTNode[Value] | None, result: list[Value]) -> None:
        if node is not None:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.value)
