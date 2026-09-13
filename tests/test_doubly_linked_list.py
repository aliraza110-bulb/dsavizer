import pytest

from data_structures.doubly_linked_list import DoublyLinkedList


def test_doubly_linked_list_keeps_both_directions() -> None:
    linked_list = DoublyLinkedList[int]()
    linked_list.insert_end(10)
    linked_list.insert_end(30)
    linked_list.insert_at(1, 20)

    assert linked_list.traverse_forward() == [10, 20, 30]
    assert linked_list.traverse_backward() == [30, 20, 10]
    assert linked_list.head is not None
    assert linked_list.head.previous is None
    assert linked_list.tail is not None
    assert linked_list.tail.next is None


def test_doubly_linked_list_delete_updates_head_tail_and_links() -> None:
    linked_list = DoublyLinkedList([10, 20, 30])

    assert linked_list.delete_at(0) == 10
    assert linked_list.delete_at(1) == 30
    assert linked_list.traverse_forward() == [20]
    assert linked_list.traverse_backward() == [20]
    assert linked_list.head is linked_list.tail
    assert linked_list.head is not None
    assert linked_list.head.previous is None
    assert linked_list.head.next is None


def test_doubly_linked_list_rejects_invalid_positions() -> None:
    linked_list = DoublyLinkedList[int]()

    with pytest.raises(IndexError):
        linked_list.insert_at(-1, 10)
    with pytest.raises(IndexError):
        linked_list.delete_at(0)
