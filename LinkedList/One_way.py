"""
@Date: 2021/4/12, 22:28
@Author: Chen Zhang
@Brief: 单向链表的实现

"""
from Node import *


class OnewayLinkedlist:

    def __init__(self, sourceCollection=None):
        self.head = None  # Pointer to the head
        self.tail = None  # Pointer to the tail
        self._num = 0  # Amount of nodes

        if sourceCollection:
            for item in sourceCollection:
                self.add(item)

    def __len__(self):
        return self._num

    def __str__(self):
        string = []
        cursor = self.head
        while cursor:
            string.append(cursor.val)
            cursor = cursor.next
        return ' '.join(map(str, string))

    def is_Empty(self):
        return len(self) == 0

    def __add__(self, other):
        assert isinstance(other, OnewayLinkedlist), 'Wrong type'
        new_linked_list = OnewayLinkedlist(self)
        new_linked_list.tail.next = other.head
        return new_linked_list

    def __eq__(self, other):
        if not isinstance(other, OnewayLinkedlist):  # same type
            return False
        if len(self) != len(other):  # same length
            return False
        cursor_1, cursor_2 = self.head, other.head  # same nodes
        while cursor_1:
            if cursor_1.val != cursor_2.val:
                return False
            cursor_1, cursor_2 = cursor_1.next, cursor_2.next
        return True

    def __iter__(self):
        cursor = self.head
        while cursor:
            yield cursor
            cursor = cursor.next

    def __contains__(self, item):
        cursor = self.head
        while cursor:
            if item == cursor.val:
                return True
            cursor = cursor.next
        return False

    def add(self, value):
        if self._num:  # linked_list is not empty
            self.tail.next = Node(value)  # create new node to the end
            self.tail = self.tail.next  # move tail pointer
        else:
            self.head = Node(value)  # create new node and set head pointer
            self.tail = self.head  # set tail pointer
        self._num += 1

    def delete(self, target):
        cursor = self.head
        if cursor.val == target:
            self.head = self.head.next
        while cursor.next:
            if cursor.next.val == target:
                cursor.next = cursor.next.next
                print('Successfully delete %s!', str(target))
                return
        raise ValueError('%s is not in this linked list!')


if __name__ == '__main__':
    temp = [1, 2, 3, 4]
    s = OnewayLinkedlist(temp)
    print(s)
    print(len(s))
    t = OnewayLinkedlist()
    t.add(5)
    print(s == t)
