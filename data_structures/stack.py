"""A small LIFO stack implementation for the visualizer."""

from collections.abc import Iterable
from typing import Generic, TypeVar


Value = TypeVar("Value")


class Stack(Generic[Value]):
    """Last-in, first-out collection backed by a Python list."""

    def __init__(self, values: Iterable[Value] | None = None) -> None:
        self._items: list[Value] = list(values or [])

    def push(self, value: Value) -> None:
        """Place a value on top of the stack."""
        self._items.append(value)

    def pop(self) -> Value:
        """Remove and return the top value."""
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack.")
        return self._items.pop()

    def peek(self) -> Value:
        """Return the top value without removing it."""
        if self.is_empty():
            raise IndexError("Cannot peek at an empty stack.")
        return self._items[-1]

    def clear(self) -> None:
        """Remove every value from the stack."""
        self._items.clear()

    def is_empty(self) -> bool:
        """Return whether the stack contains no values."""
        return not self._items

    def to_list(self) -> list[Value]:
        """Return a copy ordered from bottom to top."""
        return self._items.copy()

    def __len__(self) -> int:
        return len(self._items)
