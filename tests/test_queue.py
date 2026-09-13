import pytest

from data_structures.queue import Queue


def test_queue_is_fifo() -> None:
    queue = Queue([10, 20])
    queue.enqueue(30)

    assert queue.to_list() == [10, 20, 30]
    assert queue.dequeue() == 10
    assert queue.peek() == 20
    assert len(queue) == 2


def test_queue_clear_and_empty_state() -> None:
    queue = Queue([1, 2])

    queue.clear()

    assert queue.is_empty()
    assert queue.to_list() == []


def test_queue_rejects_empty_operations() -> None:
    queue = Queue()

    with pytest.raises(IndexError, match="empty queue"):
        queue.dequeue()
    with pytest.raises(IndexError, match="empty queue"):
        queue.peek()
