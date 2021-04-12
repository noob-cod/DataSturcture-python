"""
File: queue_array.py
Author: Chen Zhang

Queue implement based on array
"""
from arrays import Array


class ArrayQueue(object):
    """An array-based queue implement"""

    default_capacity = 10

    # Constructor
    def __init__(self, source_collection=None):
        """Set the initial state of self, witch includes the contents of sourceCollection, if it's present"""
        self._capacity = ArrayQueue.default_capacity
        self._items = Array(self._capacity)
        self._size = 0
        self._front = None
        self._rear = None

        if source_collection is not None:
            for item in source_collection:
                self.add(item)

    # Mutator
    def isEmpty(self):
        """Return True if len(self)==0, or False otherwise"""
        return len(self) == 0

    def __len__(self):
        """Return the number of items in self"""
        return self._size

    def __str__(self):
        """Return the string representation of self"""
        return '{' + ', '.join(map(str, self)) + '}'

    def __iter__(self):
        """Supports iteration over a view of self"""
        cursor = self._front
        if self._front <= self._rear:
            while cursor <= self._rear:
                yield self._items[cursor]
                cursor += 1
        else:
            # self._front > self._rear
            for i in range(cursor, self._capacity):
                yield self._items[i]
            for j in range(0, self._rear + 1):
                yield self._items[j]

    def __contains__(self, target):
        """Return True if item is in self, or False otherwise"""
        for item in iter(self):
            if item == target:
                return True
        return False

    def __eq__(self, other):
        """Return True if self equals other, or False otherwise"""
        if type(self) != type(other):
            return False
        elif len(self) == len(other):
            for item in other:
                if item not in self:
                    return False
        else:
            return False
        return True

    def __add__(self, other):
        """Return a new queue containing self and other"""
        result = ArrayQueue(self)
        for item in other:
            result.add(item)
        return result

    def clear(self):
        """Make self become empty"""
        self._items = Array(self._capacity)
        self._size = 0
        self._front = None
        self._rear = None

    # Accessor
    def peek(self):
        """
        Precondition: Self is not empty
        Raise: ValueError if self if empty
        Postcondition: Head item in self is returned
        """
        if len(self) == 0:
            raise ValueError('Queue is empty!')
        item = self._items[self._front]
        return item

    def add(self, item):
        """
        If self._rear == self.capacity - 1 and self._size < self._capacity, reset self._rear as 0;
        if self._rear == self.capacity - 1 and self._size == self._capacity, capacity needs to be expanded.
        """
        if self.isEmpty():
            self._front = 0
        if self._rear == self._capacity - 1 and self._size < self._capacity:
            self._rear = 0
            self._items[self._rear] = item
            self._size += 1
        else:
            if self._size == self._capacity:
                self._capacity += ArrayQueue.default_capacity
                new_items = Array(self._capacity, source_collection=self._items)  # construct a new larger array
                self._items = new_items
            self._rear += 1
            self._items[self._rear] = item
            self._size += 1

    def pop(self):
        """
        Precondition: Self is not empty
        Raise: ValueError if self if empty
        Postcondition: Head item in self is returned
        """
        if len(self) == 0:
            raise ValueError('Queue is empty!')
        item = self._items[self._front]
        if self._front == self._capacity - 1:
            self._front = 0
        else:
            self._front += 1
        return item
