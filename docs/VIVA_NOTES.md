# Viva Notes

## Queue

A queue is FIFO. The list stores the front at index zero and the rear at the last index. Enqueue appends in O(1); dequeue shifts the list and is O(n) in this educational representation. Empty dequeue/peek operations raise clear errors.

## Stack

A stack is LIFO. The list end is the top, so push, pop, and peek are O(1) amortized. Empty pop/peek operations are rejected.

## Linked Lists

A singly linked node stores a value and a next pointer. A doubly linked node stores previous and next pointers, allowing reverse traversal. Positional insertion and deletion require locating a node and are O(n). The doubly linked list maintains both head and tail.

## General Tree

The implementation uses first-child/next-sibling links to represent arbitrary children. This makes preorder, postorder, and level order direct. Inorder is defined only for the left-child/right-sibling binary projection, which is why the UI documents that convention.

## BST

The BST invariant is left values less than the node and right values greater than the node. Inorder traversal is sorted. Deleting a node with two children copies the inorder successor, then removes that successor. Runtime depends on height: average O(log n), worst O(n).

## AVL

An AVL tree is a self-balancing BST. Each node stores height, and balance factor is height(left) minus height(right). When the absolute factor exceeds one, the implementation performs a real LL, RR, LR, or RL rotation. This keeps height O(log n).

## B+ Tree

All keys are stored in linked leaf nodes; internal keys are separators used for routing. When a node exceeds its capacity, it splits and promotes a separator. The implementation is intentionally small and in-memory for visualization, not a production database index.

## Graph

The graph is undirected and uses adjacency sets. BFS uses a queue and explores by layers; DFS explores one branch before backtracking. Both are O(V + E). The dashboard records traversal order as step metadata.

## Hash Table

The table hashes an integer with `key % capacity`. A collision advances through slots using linear probing. Deletion writes a tombstone so later searches do not stop prematurely at the deleted slot. Average operations are O(1), but the worst case is O(n) as the table fills.

## Dash Questions

- Why are algorithms outside Dash? To test them without a browser and keep responsibilities separate.
- Why use `dcc.Store`? It keeps browser-session state JSON-compatible and lets callbacks rebuild plain Python objects.
- How are errors handled? Expected domain errors are caught by the operation callback and displayed in the status panel.
- Why step metadata? Traversals produce an ordered list, and Previous/Next selects the current visual step without requiring fragile animation timing.
