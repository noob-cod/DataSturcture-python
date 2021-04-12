"""
File: stackinterface.py
Author: Chen Zhang
"""


class StackInterface(object):
    """Interface for all stack types"""

    # Constructor
    def __init__(self, sourceCollection):
        """Sets the initial state of self, witch includes the contents of sourceCollection, if it's present."""
        pass

    # Accessors
    def isEmpty(self):
        """Returns True if len(self) == 0, or False otherwise."""
        return 0

    def __str__(self):
        """Returns the string representation of self."""
        return ""

    def __len__(self):
        """Returns the number of items in self."""
        return 0

    def __add__(self, other):
        """Returns a new stack containing contents of self and others."""
        return 0

    def __eq__(self, other):
        """Returns True if self equals other, or False otherwise."""
        return 0

    def __iter__(self):
        """Supports iteration over a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if item in self, or False otherwise."""
        return None

    def peek(self):
        """
        Precondition: Self is not empty.
        Raise: ValueError if self is empty.
        Postcondition:  Top item in self is returned and remained in self.
        """
        return None

    # Mutators
    def push(self, item):
        """Push item on the top of self"""
        return None

    def pop(self):
        """
        Precondition: Self is not empty.
        Raise: ValueError if self is empty.
        Postcondition: Top item in self is returned and removed.
        """
        return None



    def clear(self):
        """Make self become empty"""
        pass
