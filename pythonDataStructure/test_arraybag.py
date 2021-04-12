"""
File: test_arraybag.py
Author: Ken Lambert
"""
from arrays import Array
from abstractbag import AbstractBag

class ArrayBag(AbstractBag):
    """An array-based bag implementation"""

    # Class variable
    DEFAULT_CAPACITY = 10

    # Constructor
    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the contents of sourceCollection, if it's present."""
        self._items = Array(ArrayBag.DEFAULT_CAPACITY)
        AbstractBag.__init__(self, sourceCollection)
        if sourceCollection:
            for item in sourceCollection:
                self.add(item)

    # Accessor methods
    def __iter__(self):
        """Supports iteration over a view of self"""
        cursor = 0
        while cursor < len(self):
            yield self._items[cursor]
            cursor += 1
    # Mutator methods
    def clear(self):
        """Makes self become empty"""
        self._items = Array(ArrayBag.DEFAULT_CAPACITY)
        self._size = 0

    def add(self, item):
        """Add items to self"""
        # Check array memory here and increase it if necessary
        self._items[len(self)] = item
        self._size += 1

    def remove(self, item):
        """
        Precondition: items is in self
        Raises: KeyError if item is not in self
        Postcondition: item is removed from self
        """
        # Check precondition and raise if necessary
        if item not in self:
            raise KeyError(str(item) + ' not in bag')

        # Search for index of target item
        targetIndex = 0
        for targetItem in self:
            if targetItem == item:
                break
            targetIndex += 1

        # Shift items to the left of target up by one position
        for i in range(targetIndex, len(self) - 1):
            self._items[i] = self._items[i+1]

        # Decrement logical size
        self._size -= 1
        # Check memory here and decrease it if necessary
