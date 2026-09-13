"""A small FIFO queue implementation for the visualizer."""

from collections.abc import Iterable
from typing import Generic, TypeVar


Value = TypeVar("Value")


class Queue(Generic[Value]):
    """First-in, first-out collection backed by a Python list.

    The list representation keeps the implementation easy to inspect. Removing
    the first item is O(n) because the remaining items shift left.
    """

    def __init__(self, values: Iterable[Value] | None = None) -> None:
        self._items: list[Value] = list(values or [])

    def enqueue(self, value: Value) -> None:
        """Add a value at the rear of the queue."""
        self._items.append(value)

    def dequeue(self) -> Value:
        """Remove and return the value at the front."""
        if self.is_empty():
            raise IndexError("Cannot dequeue from an empty queue.")
        return self._items.pop(0)

    def peek(self) -> Value:
        """Return the front value without removing it."""
        if self.is_empty():
            raise IndexError("Cannot peek at an empty queue.")
        return self._items[0]

    def clear(self) -> None:
        """Remove every value from the queue."""
        self._items.clear()

    def is_empty(self) -> bool:
        """Return whether the queue contains no values."""
        return not self._items

    def to_list(self) -> list[Value]:
        """Return a copy ordered from front to rear."""
        return self._items.copy()

    def __len__(self) -> int:
        return len(self._items)
