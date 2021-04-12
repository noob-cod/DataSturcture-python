"""
File: queue_priority_linked.py
Author: Chen Zhang
"""
from node import Node
from queue_linked import LinkedQueue


class LinkedPriorityQueue(LinkedQueue):
    """A Link-based priority queue implementation"""

    def __init__(self, source_collection=None):
        """Set the initial state of self, which includes the contents of source_collection, if it's present"""
        # LinkedQueue.__init__(self, source_collection)
        super().__init__(source_collection)

    def add(self, newItem):
        """Inserts newItem after items of greater or equal priority or ahead of items of lesser priority"""
        global trailer
        if self.isEmpty() or newItem >= self._rear.data:
            # New item goes at rear
            LinkedQueue.add(self, newItem)
        else:
            # Search for a  position where it's less
            probe = self._front
            while newItem >= probe.data:
                trailer = probe
                probe = probe.next
            newNode = Node(newItem, probe)
            if probe == self._front:
                # New item goes at front
                self._front = newNode
            else:
                # New item goes between two nodes
                trailer.next = newNode
            self._size += 1


class Comparable(object):
    """Wrapper class for items that are not comparable"""

    def __init__(self, data, priority=1):
        self._data = data
        self._priority = priority

    def __str__(self):
        """Returns the string rep of the contained datum"""
        return str(self._data)

    def __eq__(self, other):
        """Returns True if the contained priorities are equal or False otherwise"""
        if self is other: return True
        if type(self) != type(other): return False
        return self._priority == other._priority

    def __lt__(self, other):
        """Return True if self's priority < other's priority, or False otherwise"""
        return self._priority < other._priority

    def __le__(self, other):
        """Return True if self's priority <= other's priority, or False otherwise"""
        return self._priority <= other._priority

    def getDate(self):
        """Return the contained datum"""
        return self._data

    def getPriority(self):
        """Return the contained priority"""
        return self._priority
