"""
@Date: Friday, March 12, 2021
@Author: Chen Zhang
@Brief: 图数据结构的实现
"""
import numpy as np


class ArrayGraph:
    def __init__(self, sourceCollection=None):
        self._num = 0
        self.graph = np.zeros((self._num, self._num))

    def __len__(self):
        return self._num

    def is_Empty(self):
        return len(self) == 0

    def __str__(self):
        print(self.graph)

    def __eq__(self, other):
        pass

    def add(self, newNode):
        new1 = np.zeros((self._num, 1))
        self.graph = np.hstack((self.graph, new1))
        new2 = np.zeros((1, self._num+1))
        self.graph = np.vstack((self.graph, new2))

    def clear(self):
        self._num = 0
        self.graph = np.zeros((self._num, self._num))

    def to_linked(self):
        """转化为链表表示"""
        pass
