"""
File: arrays.py

An Array is like a list, but the client can use only [], len, iter, and str.

To instantiate, use
<variable> = Array(<capacity>, <optional fill value>)

The fill value is None by default
"""


class Array(object):
    """Represents an array"""

    # Constructor
    def __init__(self, capacity, source_collection=None):
        """Capacity is the static size of the array. fillValue is placed at each position"""
        self._items = list()
        self._size = 0
        for item in source_collection:
            if self._size < capacity:
                self._items.append(item)
                self._size += 1
            else:
                raise OverflowError('Capacity is not enough!')

    # Mutator
    def __len__(self):
        """-> The capacity of the array"""
        return len(self._items)
    
    def __str__(self):
        """-> The string representation of the array"""
        return str(self._items)

    # Accessor
    def __iter__(self):
        """Supports traversal with a for loop"""
        return iter(self._items)

    def __getitem__(self, index):
        """Subscript operator for access at index"""
        return self._items[index]

    def __setitem__(self, index, newItem):
        """Subscript operator for replacement at index"""
        self._items[index] = newItem
