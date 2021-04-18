"""
@Date: 2021/4/9 下午1:37
@Author: Chen Zhang
@Brief: 堆 的实现

堆的定义：
堆的特性：
"""
import abc


class Heap(abc.ABC):
    """堆的抽象类"""
    def __init__(self, sourceCollection=None):
        self._container = [None]  # 堆容器
        self._size = 0  # 堆尺寸
        self._top = None  # 堆顶
        self._bottom = None  # 堆尾

        if sourceCollection:
            for item in sourceCollection:
                self.add(item)

    @property
    def container(self):
        return self._container

    @property
    def size(self):
        return self._size

    @property
    def top(self):
        return self._top

    @property
    def bottom(self):
        return self._bottom

    def is_Empty(self):
        """Return whether self is empty"""
        return len(self) == 0

    def __len__(self):
        """Return the amount of nodes of self."""
        return self._size

    def __str__(self):
        """Return string of self"""
        if self.is_Empty():
            return '[]'
        return 'Contents of Heap: [' + ', '.join(map(str, self._container[1: self._bottom + 1])) + ']' + '\n'

    def draw(self):
        """Return the string of self."""
        if self.is_Empty():
            print('Heap is empty!')
            print()
            return
        print('=' * 50)
        print('Heap')
        self.__draw(self._top, 0, 'H', 17)
        print('=' * 50)

    def __draw(self, root, height, preStr, length):
        """递归打印二叉树"""
        if root > self._bottom:
            return
        self.__draw(root * 2 + 1, height + 1, 'V', length)
        string = preStr + str(self._container[root]) + preStr
        leftLen = (length - len(string)) // 2
        rightLen = length - len(string) - leftLen
        res = " " * leftLen + string + " " * rightLen
        print(" " * height * length + res)
        self.__draw(root * 2, height + 1, '^', length)

    @abc.abstractmethod
    def add(self, newValue):
        """Add newValue to heap"""
        pass

    @abc.abstractmethod
    def delete(self, target):
        """Delete specific node from heap"""
        pass

    @abc.abstractmethod
    def find(self, value):
        """Find value in self"""
        pass

    def clear(self):
        """Reset self"""
        self._container = [None]
        self._size = 0
        self._top = None
        self._bottom = None

    def swap(self, ind1, ind2):
        assert isinstance(ind1, int)
        assert isinstance(ind2, int)
        assert (ind1 <= self._bottom) and (ind2 <= self._bottom)
        self._container[ind1], self._container[ind2] = self._container[ind2], self._container[ind1]


class MaxHeap(Heap):
    """大顶堆"""
    def add(self, newValue):
        """Add newValue to heap"""
        self.__add(newValue)

    def __add(self, newValue):
        """Add newValue"""
        self._container.append(newValue)
        self._size += 1

        if len(self) == 1:
            self._top = 1  # 重置堆顶
            self._bottom = 1
        else:
            self._bottom += 1
            ind = self._bottom
            while ind != self._top:
                if self._container[ind] > self._container[ind // 2]:
                    self._container[ind], self._container[ind // 2] = self._container[ind // 2], self._container[ind]
                    ind = ind // 2
                else:
                    break

    def delete(self, target):
        """Delete specific node from heap"""
        self._delete(target)

    def _delete(self, target):
        """Delete specific node from self"""
        ind = self.find(target)
        if ind == -1:
            raise ValueError('Not Found!')
        if ind == self._top and self._bottom == self._top:
            self._container.pop()
            self._size = 0
            self._top = None
            self._bottom = None
        elif ind == self._bottom:
            self._container.pop()
            self._size -= 1
            self._bottom -= 1
        else:
            # 将最后一个节点与待删值交换，删除最后一个节点，更新状态，并通过交换值的方式向下修复堆的性质
            self.swap(ind, self._bottom)
            self._container.pop()
            self._size -= 1
            self._bottom -= 1

            # 删除后修复堆
            while True:
                left, right = ind * 2, ind * 2 + 1
                if left > self._bottom:
                    break
                elif right > self._bottom:
                    if self._container[left] > self._container[ind]:
                        self.swap(ind, left)
                        ind = left
                    else:
                        break
                else:
                    if self._container[ind] > self._container[left] and self._container[ind] > self._container[right]:
                        break
                    else:
                        if self._container[left] >= self._container[right]:
                            tmp_ind = left
                        else:
                            tmp_ind = right
                        self.swap(ind, tmp_ind)
                        ind = tmp_ind

    def find(self, value):
        """Find value in heap"""
        return self.__find(value)

    def __find(self, value):
        """Find value in self"""
        if len(self) == 0:
            return -1
        if value > self._container[self._top]:
            return -1
        for index in range(1, self._bottom+1):
            if self._container[index] == value:
                return index
        return -1


class MinHeap(Heap):
    """小顶堆"""
    def add(self, newValue):
        """Add newValue to heap"""
        self.__add(newValue)

    def __add(self, newValue):
        """Add newValue"""
        self._container.append(newValue)
        self._size += 1

        if len(self) == 1:
            self._top = 1  # 重置堆顶
            self._bottom = 1
        else:
            self._bottom += 1
            ind = self._bottom
            while ind != self._top:
                if self._container[ind] < self._container[ind // 2]:
                    self._container[ind], self._container[ind // 2] = self._container[ind // 2], self._container[ind]
                    ind = ind // 2
                else:
                    break

    def delete(self, target):
        """Delete specific node from heap"""
        self._delete(target)

    def _delete(self, target):
        """Delete specific node from self"""
        ind = self.find(target)
        if ind == -1:
            raise ValueError('Not Found!')
        if ind == self._top and self._bottom == self._top:
            self._container.pop()
            self._size = 0
            self._top = None
            self._bottom = None
        elif ind == self._bottom:
            self._container.pop()
            self._size -= 1
            self._bottom -= 1
        else:
            # 将最后一个节点与待删值交换，删除最后一个节点，更新状态，并通过交换值的方式向下修复堆的性质
            self.swap(ind, self._bottom)
            self._container.pop()
            self._size -= 1
            self._bottom -= 1

            # 删除后修复堆
            while True:
                left, right = ind * 2, ind * 2 + 1
                if left > self._bottom:
                    break
                elif right > self._bottom:
                    if self._container[left] < self._container[ind]:
                        self.swap(ind, left)
                        ind = left
                    else:
                        break
                else:
                    if self._container[ind] < self._container[left] and self._container[ind] < self._container[right]:
                        break
                    else:
                        if self._container[left] < self._container[right]:
                            tmp_ind = left
                        else:
                            tmp_ind = right
                        self.swap(ind, tmp_ind)
                        ind = tmp_ind

    def find(self, value):
        """Find value in heap"""
        return self.__find(value)

    def __find(self, value):
        """Find value in self"""
        if len(self) == 0:
            return -1
        if value > self._container[self._top]:
            return -1
        for index in range(1, self._bottom+1):
            if self._container[index] == value:
                return index
        return -1


if __name__ == '__main__':
    test_list = [3, 7, 1, 4, 5, 6, 2, 8, 9, 10, 11, 12]

    max_heap = MaxHeap(test_list)
    max_heap.draw()
    print(max_heap)

    min_heap = MinHeap(test_list)
    min_heap.draw()
    print(min_heap)

    heap = MinHeap()
    heap.draw()
    print(heap)
