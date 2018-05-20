"""
    Holds all node types in use for any CraftBin util.

    Author: CraftSpider
"""


class Node:
    """
        Primary basic node structure, linkable in two directions.
    :slot prev: Previous node in the list. Type: None, Node
    :slot data: Data held in the current node. Type: Object
    :slot next: Next node in the list. Type: None, Node
    """
    __slots__ = ("prev", "data", "next")

    def __init__(self, prev, data, next):
        self.prev = prev
        self.data = data
        self.next = next
