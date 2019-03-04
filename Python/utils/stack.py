"""
    Stack structure file, for creating and using a stack.

    Author: CraftSpider
"""

from .node import Node


class Stack:
    """
        Top of a stack, holds the front node and the size of the stack.
    :slot top: Reference to the top node in the stack. Type: None, Node
    :slot size: Total size of the stack. Type: Int.
    """
    __slots__ = ("head", "size")

    def __init__(self, head):
        self.head = head
        self.size = 0

    def push(self, dta):
        """
                Push a node onto the stack.
            :param stk: Stack to modify. Type: Stack
            :param dta: Data to add onto the stack. Type: Object
            :post-conditions: Stack has data now on the top.
        """
        nd = Node(None, dta, self.head)
        self.head = nd
        self.size += 1

    def top(self):
        """
            Peeks at the top node in the stack.
        :pre-conditions: Stack has at least one item.
        :param stk: Stack to check the top of. Type: Stack
        :return: Top item in the stack. Type: Object
        """
        if self.size == 0:
            raise IndexError("Top of stack out of range.")
        return self.head.data

    def pop(self):
        """
            Returns and deletes the top node of a stack.
        :pre-conditions: Stack has at least one item
        :param stk: Stack to alter. Type: Stack
        :return: Top item in the stack. Type: Object
        :post-conditions: Top item in stack is now top.next
        """
        if self.size == 0:
            raise IndexError("Top of stack out of range.")
        dta = self.head.data
        self.head = self.head.next
        self.size -= 1
        return dta

    def empty(self):
        """
            Empties an already existing stack.
        :param stk: Stack to empty. Type: Stack
        :post-conditions: Stack passed in has no items and zero size.
        """
        self.head = None
        self.size = 0


def create_stack():
    """
        Creates and returns an empty stack.
    :return: New, empty stack. Type: Stack
    """
    return Stack(None)
