"""Complexity metadata displayed by the dashboard."""

COMPLEXITIES = {
    "Queue": {"Enqueue": ("O(1)", "O(n)"), "Dequeue": ("O(n)", "O(n)"), "Peek": ("O(1)", "O(n)"), "Display": ("O(n)", "O(n)")},
    "Stack": {"Push": ("O(1) amortized", "O(n)"), "Pop": ("O(1) amortized", "O(n)"), "Peek": ("O(1)", "O(n)"), "Display": ("O(n)", "O(n)")},
    "Singly Linked List": {"Insert Beginning": ("O(1)", "O(n)"), "Insert End": ("O(n)", "O(n)"), "Insert Position": ("O(n)", "O(n)"), "Delete": ("O(n)", "O(n)"), "Search": ("O(n)", "O(n)"), "Traverse": ("O(n)", "O(n)")},
    "Doubly Linked List": {"Insert Beginning": ("O(1)", "O(n)"), "Insert End": ("O(1)", "O(n)"), "Insert Position": ("O(n)", "O(n)"), "Delete": ("O(n)", "O(n)"), "Search": ("O(n)", "O(n)"), "Forward Traversal": ("O(n)", "O(n)"), "Backward Traversal": ("O(n)", "O(n)")},
    "General Tree": {"Add Node": ("O(n)", "O(n)"), "Delete Node": ("O(n)", "O(n)"), "Preorder": ("O(n)", "O(n)"), "Inorder": ("O(n)", "O(n)"), "Postorder": ("O(n)", "O(n)"), "Level Order": ("O(n)", "O(n)")},
    "Binary Search Tree": {"Insert": ("O(log n) average, O(n) worst", "O(n)"), "Search": ("O(log n) average, O(n) worst", "O(1)"), "Delete": ("O(log n) average, O(n) worst", "O(n)"), "Minimum": ("O(h)", "O(1)"), "Maximum": ("O(h)", "O(1)"), "Inorder": ("O(n)", "O(n)"), "Preorder": ("O(n)", "O(n)"), "Postorder": ("O(n)", "O(n)"), "Level Order": ("O(n)", "O(n)")},
    "AVL Tree": {"Insert": ("O(log n)", "O(log n)"), "Search": ("O(log n)", "O(1)"), "Delete": ("O(log n)", "O(log n)"), "Height": ("O(1)", "O(1)")},
    "B+ Tree": {"Insert": ("O(log n)", "O(log n)"), "Search": ("O(log n)", "O(1)"), "Leaf Traversal": ("O(n)", "O(1)")},
    "Graph": {"Add Vertex": ("O(1)", "O(V)"), "Add Edge": ("O(1)", "O(V + E)"), "Delete Vertex": ("O(V)", "O(V + E)"), "Delete Edge": ("O(1)", "O(V + E)"), "BFS": ("O(V + E)", "O(V)"), "DFS": ("O(V + E)", "O(V)")},
    "Hash Table": {"Insert": ("O(1) average, O(n) worst", "O(n)"), "Search": ("O(1) average, O(n) worst", "O(1)"), "Delete": ("O(1) average, O(n) worst", "O(1)"), "Display": ("O(n)", "O(n)")},
}
