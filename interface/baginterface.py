"""
File: baginterface.py
Author: Ken Lambert
"""


class BagInterface(object):
    """Interface for all bag types"""

    # Constructor
    def __init__(self):
        """Sets the initial state of self, which includes the contents of sourceCollection, if it's present."""
        pass

    # Accessor methods
    def isEmpty(self):
        """Return True if len(self)==0, or False otherwise"""
        pass

    def __len__(self):
        """Returns the number of items in self"""
        return 0

    def __str__(self):
        """Returns the string representation of self"""
        return ""

    def __iter__(self):
        """Supports iteration over a view of self"""
        return None

    def __add__(self, other):
        """Returns a new bag containing the contents of self and others"""
        return None

    def __eq__(self, other):
        """Returns True if self equals other, or False otherwise"""
        return False

    # Mutator methods
    def clear(self):
        """Makes self become empty"""
        pass

    def add(self):
        """Add items to self"""
        pass

    def remove(self, item):
        """
        Precondition: items is in self
        Raises: KeyError if item is not in self
        Postcondition: item is removed from self
        """
        pass
