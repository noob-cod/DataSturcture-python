"""
File: node.py
Author: Ken Lambert
"""


class Node(object):
    """Represent a singly linked node"""

    # Constructor
    def __init__(self, data, next=None):
        """Instantiates a Node with a default next of None"""
        self.data = data
        self.next = next

    # Accessor

    # Mutator
    def add(self, item):
        self.data = item
