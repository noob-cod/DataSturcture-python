"""
File: arraystack.py
Author: Chen Zhang

基于数组(array)的栈(stack)的实现
"""
from arrays import Array


class ArrayStack(object):
    """An array-based stack implementation """

    DEFAULTCAPACITY = 10  # 栈的默认容量

    # Constructor 构建器
    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, witch includes the contents of sourceCollection, if it's present."""
        self._items = Array(ArrayStack.DEFAULTCAPACITY)  # 栈的基本数据结构
        self._size = 0  # 栈使用量
        self._mark = 0  # 栈容量标志，若为0则表示栈的实际容量等于默认容量，若不为0则表示栈的实际容量大于默认容量
        if sourceCollection:  # 若给定了初始元素，则将其添加到栈中
            for item in sourceCollection:
                self.push(item)

    # Accessors 访问器，访问对象的属性或元素，不修改对象
    def isEmpty(self):
        """Returns True if len(self) == 0, or False otherwise."""
        return len(self) == 0

    def __str__(self):  # 魔法函数，str()
        """Returns the string representation of self."""
        return "{" + ', '.join(map(str, self)) + "}"

    def __len__(self):  # 魔法函数，len()
        """Returns the number of items in self."""
        return self._size

    def __add__(self, other):  # 魔法函数，+
        """Returns a new stack containing contents of self and others."""
        result = ArrayStack(self)  # 将self作为新创建的result的sourceCollection参数传入，result中包含了self内元素
        for item in other:  # 将other中元素传入新建的result栈中
            result.push(item)
        return result

    def __eq__(self, other):  # 魔法函数，==
        """Returns True if self equals other, or False otherwise."""
        if type(self) != type(other):  # 判断类
            return False
        elif len(self) == len(other):  # 判断长度
            for item in other:  # 逐项判断
                if item not in self:
                    return False
        else:
            return False
        return True

    def __iter__(self):  # 魔法函数，可迭代对象或iter()
        """Supports iteration over a view of self."""
        cursor = 0
        while cursor < len(self):
            yield self._items[cursor]  # 迭代器
            cursor += 1

    def __contains__(self, item):  # 魔法函数, in
        """Returns True if item in self, or False otherwise."""
        for i in iter(self):
            if i == item:
                return True
        return False

    def peek(self):
        """
        Precondition: Self is not empty.
        Raise: ValueError if self is empty.
        Postcondition:  Top item in self is returned and remained in self.
        """
        if len(self) == 0:
            raise ValueError('Stack is empty')
        item = self._items[len(self)-1]  # 数组的最后一个元素
        return item

    # Mutators 设置器，对对象的属性或内容进行修改对象
    def push(self, item):
        """Push item on the top of self"""
        if len(self) == ArrayStack.DEFAULTCAPACITY * (self._mark + 1):  # 若栈容量已满，则需要扩大栈的容量
            new_items = Array(ArrayStack.DEFAULTCAPACITY * (self._mark + 2))  # 扩大一个默认容量大小的容量
            self._mark += 1  # 栈容量标志增加
            for n, items in enumerate(self._items):  # 栈内元素转移
                new_items[n] = items
            self._items = new_items
        self._items[len(self)] = item
        self._size += 1

    def pop(self):
        """
        Precondition: Self is not empty.
        Raise: ValueError if self is empty.
        Postcondition: Top item in self is returned and removed.
        """
        if len(self) == 0:
            raise ValueError('Stack is empty')
        item = self._items[-1]
        self._items = self._items[:-1]  # 弹出栈顶元素
        self._size -= 1  # 栈的使用量减1
        return item

    def clear(self):
        """Make self become empty"""
        self._items = Array(ArrayStack.DEFAULTCAPACITY)
        self._size = 0
