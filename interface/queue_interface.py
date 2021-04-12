"""
File: queue_interface.py
Author: Chen Zhang
"""


class queue(object):
    """Interface for queue type"""

    # Constructor
    def __init__(self, source_collection=None):
        """Set the initial state of self, witch includes the contents of sourceCollection, if it's present"""
        pass

    # Mutator
    def isEmpty(self):
        """Return True if len(self)==0, or False otherwise"""
        return 0

    def __len__(self):
        """Return the number of items in self"""
        return 0

    def __str__(self):
        """Return the string representation of self"""
        return ""

    def __iter__(self):
        """Supports iteration over a view of self"""
        return 0

    def __contains__(self, item):
        """Return True if item is in self, or False otherwise"""
        return bool

    def __eq__(self, other):
        """Return True if self equals other, or False otherwise"""
        return bool

    def __add__(self, other):
        """Return a new queue containing self and other"""
        return 0

    def clear(self):
        """Make self become empty"""
        pass

    # Accessor
    def peek(self):
        """
        Precondition: Self is not empty
        Raise: ValueError if self if empty
        Postcondition: Head item in self is returned
        """
        return 0

    def add(self, item):
        """Add item to tail of self"""
        pass

    def pop(self):
        """
        Precondition: Self is not empty
        Raise: ValueError if self if empty
        Postcondition: Head item in self is returned
        """
        return 0
