"""
File: test_linkedbag.py
Author: Ken Lambert
"""
from node import Node
from abstractbag import AbstractBag


class LinkedBag(AbstractBag):
    """A linked-based bag implementation"""

    # Constructor
    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the contents of sourceCollection, if it's present."""
        self._items = Node(None)
        AbstractBag.__init__(self, sourceCollection)
        if sourceCollection:
            for item in sourceCollection:
                self.add(item)

    # Accessor methods
    def __iter__(self):
        """Supports iteration over a view of self"""
        cursor = self._items
        while cursor.data is not None:
            yield cursor.data
            cursor = cursor.next

    # Mutator methods
    def clear(self):
        """Makes self become empty"""
        self._items = Node(None)
        self._size = 0

    def add(self, item):
        """Add items to self"""
        self._items = Node(item, self._items)
        self._size += 1

    def remove(self, item):
        """
        Precondition: items is in self
        Raises: KeyError if item is not in self
        Postcondition: item is removed from self
        """
        # Check precondition and raise if necessary
        if item not in self:
            raise KeyError(str(item) + ' is not in bag')
        # Search for the node containing the target item
        # Probe will point to the target node, and trailer will point to the one before it, if it exist
        probe = self._items
        trailer = None
        for targetItem in self:
            if targetItem == item:
                break
            trailer = probe
            probe = probe.next

        # Unhook the node to be deleted, either teh fist one or the one thereafter
        if probe == self._items:
            self._items = self._items.next
        else:
            trailer.next = probe.next
        # Decrement logical size
        self._size -= 1
