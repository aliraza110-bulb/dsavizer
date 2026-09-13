"""Self-balancing AVL tree implementation."""

from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Generic, TypeVar


Value = TypeVar("Value")


@dataclass
class AVLNode(Generic[Value]):
    value: Value
    left: "AVLNode[Value] | None" = None
    right: "AVLNode[Value] | None" = None
    height: int = 1


class AVLTree(Generic[Value]):
    """BST that maintains an absolute balance factor of at most one."""

    def __init__(self, values: Iterable[Value] | None = None) -> None:
        self.root: AVLNode[Value] | None = None
        self.last_rotation: str | None = None
        for value in values or []:
            self.insert(value)

    def insert(self, value: Value) -> str | None:
        self.last_rotation = None
        self.root = self._insert(self.root, value)
        return self.last_rotation

    def delete(self, value: Value) -> str | None:
        self.last_rotation = None
        self.root, deleted = self._delete(self.root, value)
        if not deleted:
            raise KeyError(f"Value {value!r} was not found.")
        return self.last_rotation

    def search(self, value: Value) -> bool:
        current = self.root
        while current is not None:
            if value == current.value:
                return True
            current = current.left if value < current.value else current.right
        return False

    def height(self) -> int:
        return self._height(self.root)

    def balance_factor(self, node: AVLNode[Value] | None) -> int:
        if node is None:
            return 0
        return self._height(node.left) - self._height(node.right)

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
        pending: deque[AVLNode[Value]] = deque([self.root])
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
        self.last_rotation = None

    def _insert(self, node: AVLNode[Value] | None, value: Value) -> AVLNode[Value]:
        if node is None:
            return AVLNode(value)
        if value == node.value:
            raise ValueError(f"Value {value!r} already exists in the tree.")
        if value < node.value:
            node.left = self._insert(node.left, value)
        else:
            node.right = self._insert(node.right, value)
        self._update_height(node)
        return self._rebalance(node, value)

    def _delete(
        self, node: AVLNode[Value] | None, value: Value
    ) -> tuple[AVLNode[Value] | None, bool]:
        if node is None:
            return None, False
        if value < node.value:
            node.left, deleted = self._delete(node.left, value)
        elif value > node.value:
            node.right, deleted = self._delete(node.right, value)
        else:
            deleted = True
            if node.left is None:
                return node.right, True
            if node.right is None:
                return node.left, True
            successor = self._minimum(node.right)
            node.value = successor.value
            node.right, _ = self._delete(node.right, successor.value)
        if not deleted:
            return node, False
        self._update_height(node)
        return self._rebalance_after_delete(node), True

    def _rebalance(self, node: AVLNode[Value], inserted: Value) -> AVLNode[Value]:
        factor = self.balance_factor(node)
        if factor > 1:
            if inserted < node.left.value:  # type: ignore[union-attr]
                self.last_rotation = "LL"
                return self._rotate_right(node)
            self.last_rotation = "LR"
            node.left = self._rotate_left(node.left)  # type: ignore[arg-type]
            return self._rotate_right(node)
        if factor < -1:
            if inserted > node.right.value:  # type: ignore[union-attr]
                self.last_rotation = "RR"
                return self._rotate_left(node)
            self.last_rotation = "RL"
            node.right = self._rotate_right(node.right)  # type: ignore[arg-type]
            return self._rotate_left(node)
        return node

    def _rebalance_after_delete(self, node: AVLNode[Value]) -> AVLNode[Value]:
        factor = self.balance_factor(node)
        if factor > 1:
            if self.balance_factor(node.left) >= 0:
                self.last_rotation = "LL"
                return self._rotate_right(node)
            self.last_rotation = "LR"
            node.left = self._rotate_left(node.left)  # type: ignore[arg-type]
            return self._rotate_right(node)
        if factor < -1:
            if self.balance_factor(node.right) <= 0:
                self.last_rotation = "RR"
                return self._rotate_left(node)
            self.last_rotation = "RL"
            node.right = self._rotate_right(node.right)  # type: ignore[arg-type]
            return self._rotate_left(node)
        return node

    @staticmethod
    def _height(node: AVLNode[Value] | None) -> int:
        return node.height if node is not None else 0

    def _update_height(self, node: AVLNode[Value]) -> None:
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _rotate_left(self, node: AVLNode[Value]) -> AVLNode[Value]:
        pivot = node.right
        assert pivot is not None
        node.right = pivot.left
        pivot.left = node
        self._update_height(node)
        self._update_height(pivot)
        return pivot

    def _rotate_right(self, node: AVLNode[Value]) -> AVLNode[Value]:
        pivot = node.left
        assert pivot is not None
        node.left = pivot.right
        pivot.right = node
        self._update_height(node)
        self._update_height(pivot)
        return pivot

    @staticmethod
    def _minimum(node: AVLNode[Value]) -> AVLNode[Value]:
        while node.left is not None:
            node = node.left
        return node

    def _inorder(self, node: AVLNode[Value] | None, result: list[Value]) -> None:
        if node is not None:
            self._inorder(node.left, result)
            result.append(node.value)
            self._inorder(node.right, result)

    def _preorder(self, node: AVLNode[Value] | None, result: list[Value]) -> None:
        if node is not None:
            result.append(node.value)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def _postorder(self, node: AVLNode[Value] | None, result: list[Value]) -> None:
        if node is not None:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.value)
