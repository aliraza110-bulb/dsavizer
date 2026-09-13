import pytest

from data_structures.stack import Stack


def test_stack_is_lifo() -> None:
    stack = Stack([10, 20])
    stack.push(30)

    assert stack.to_list() == [10, 20, 30]
    assert stack.pop() == 30
    assert stack.peek() == 20
    assert len(stack) == 2


def test_stack_clear_and_empty_state() -> None:
    stack = Stack([1, 2])

    stack.clear()

    assert stack.is_empty()
    assert stack.to_list() == []


def test_stack_rejects_empty_operations() -> None:
    stack = Stack()

    with pytest.raises(IndexError, match="empty stack"):
        stack.pop()
    with pytest.raises(IndexError, match="empty stack"):
        stack.peek()
