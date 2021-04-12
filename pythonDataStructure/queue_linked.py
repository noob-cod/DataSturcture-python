"""
File: queue_linked.py
Author: Chen Zhang

Queue implement based on linked
"""
from node import Node


class LinkedQueue(object):
    """A linked-based queue implement"""

    # Constructor
    def __init__(self, source_collection=None):
        """Set the initial state of self, witch includes the contents of sourceCollection, if it's present"""
        self._size = 0
        self._front = Node(None, None)
        self._rear = Node(None, None)

        # Add contents from sourceCollection
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
        while cursor.data is not None:
            yield cursor.data
            cursor = cursor.next

    def __contains__(self, item):
        """Return True if item is in self, or False otherwise"""
        for cursor in iter(self):
            if cursor.data == item:
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
        result = LinkedQueue(self)
        for item in other:
            result.add(item)
        return result

    def clear(self):
        """Make self become empty"""
        self._front = Node(None, None)
        self._rear = Node(None, None)
        self._size = 0

    # Accessor
    def peek(self):
        """
        Precondition: Self is not empty
        Raise: ValueError if self if empty
        Post-condition: Head item in self is returned
        """
        if len(self) == 0:
            raise ValueError('Queue is empty')
        item = self._front
        return item.data

    def add(self, newItem):
        """Add newItem to the rear of the queue."""
        newNode = Node(newItem, None)
        if self.isEmpty:
            self._front = newNode
        else:
            self._rear.next = newNode
        self._rear = newNode
        self._size += 1

    def pop(self):
        """
        Precondition: Self is not empty
        Raise: ValueError if self if empty
        Postcondition: Head item in self is returned
        """
        if len(self) == 0:
            raise ValueError('Queue is empty')
        item = self._front
        self._front = self._front.next
        self._size -= 1
        return item.data
