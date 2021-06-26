"""
@Date: 2021/6/25 下午3:45
@Author: Chen Zhang
@Brief:  B树（B-树）的实现

1 B树的相关概念
    1.1 定义：百度百科 - https://baike.baidu.com/item/B%E6%A0%91/5411672?fr=aladdin
    1.2 阶数：B树节点可拥有的最多子节点的数量。B树节点的关键字数等于子节点数减1
    1.3 高度：考虑B树的高度时，不需要考虑尾部的空节点
    1.4 节点数：考虑B树的节点数时，需要考虑尾部的空节点

2 B树的一些注意事项
    2.1 B树节点的子节点数量限制
        1）2 <= 根节点子节点数 <= 阶数
        2）ceil(阶数/2) <= 内节点子节点数 <= 阶数
    2.2 B数节点的关键字数量限制
        1）1 <= 根节点关键字数 <= (阶数-1)
        2）ceil(阶数/2)-1 <= 非根节点关键字数 <= (阶数-1)

3 B树的一些特殊操作
    3.1 节点拆分
        3.1.1 场景：在B树插入操作中，当待插入的节点内关键字数量已经达到上限时触发节点拆分
        3.1.2 步骤：
            1）提取节点中第(m//2)个关键字，向上插入到父节点中（递归判断是否需要继续触发节点拆分）；
            2）将被提取关键字左右的关键字分别存放到两个节点中；
            3）将新关键字插入对应节点。
    3.2 借关键字
        3.2.1 场景：在B树的删除操作中，当待删除关键字在叶子节点中，且当前该叶子节点的关键字数量已经达到下限时触发借节点
        3.2.2 步骤：
            1）从父节点中转移一个合适的关键字到当前节点中；
            2）从兄弟节点中转移一个合适的关键字到父节点中；
            3）删除待目标关键字。
    3.3 节点合并
        3.3.1 场景：在B树的删除操作中，当关键字删除后的叶子节点的关键字数量低于下限时触发节点合并操作
        3.3.2 步骤：
            1）从父节点中转移一个合适的关键字到当前节点；
            2）将被转移关键字与其左右子节点中关键字合并为一个新的节点，作为原父节点的子节点。
"""
from math import ceil


class BNode:
    """B树节点，B树的节点没有“阶数”属性，关于阶数的检查需要在B树中实现"""
    def __init__(self, sourceCollection=None):
        """节点构造函数。"""

        self._father = None  # 父节点
        self._keys = []  # [key1, key2, ..., key(m-1)]关键字
        self._keys_nums = 0  # 当前保存的关键字数量
        self._sons = []  # [son1, son2, ... son(m)]子节点指针
        self._sons_nums = 0  # 当前保存的子节点数量

        if sourceCollection:
            for item in sourceCollection:
                self.add_key(item)

    def __contains__(self, item):
        return self.search(item) != -1

    def add_key(self, val):
        """
        添加新关键字，并返回插入位置的索引

        需要在该方法外部添加节点内关键字数量是否满足B树阶数限制的检查
        """
        return self.__add_key(val)

    def __add_key(self, val):
        # 节点为空
        if not self.keys_nums:
            self._keys.append(val)
            index = 0
        # 节点不为空
        else:
            self._keys.append(val)
            index = self.keys_nums
            while index > 0:
                if self._keys[index] >= self._keys[index - 1]:
                    break
                self._keys[index-1], self._keys[index] = self._keys[index], self._keys[index - 1]
                index -= 1

        self._keys_nums += 1
        return index

    def delete_key(self, target):
        """删除关键字"""
        self.__delete_key(target)

    def __delete_key(self, target):
        index = self.search(target)
        if index == -1:
            raise ValueNotFound(target)

        if index == self._keys_nums - 1:
            self._keys.pop()
        else:
            self._keys[index:] = self._keys[index+1:]
        self._keys_nums -= 1

        # 合并子节点
        if self._sons_nums:
            new_node = BNode(sourceCollection=(self.sons[index].keys + self.sons[index+1].keys))
            self.sons[index] = new_node
            self.__delete_node(index + 1)

    def add_node(self, newNode, index=None):
        """
        添加新的子节点，并返回该子节点的索引

        :param newNode:  BNode，新插入的子节点。
        :param index: 整型，插入节点的索引。需要在该方法外部进行是否满足B树阶数的检查。
        """
        assert isinstance(newNode, BNode), 'Mismatched type!'
        assert index is None or (index <= self.sons_nums), 'Index out of range!'
        # assert isinstance(partial(BNode, m=self.order), newNode), 'Mismatched orders!'
        self.__add_node(newNode, index)

    def __add_node(self, newNode, index=None):
        if not index or (index == self.sons_nums):
            self._sons.append(newNode)
        # 添加位置在非末尾的位置时
        else:
            self._sons[index+1:] = self._sons[index:]  # 后移
            self._sons[index] = newNode
        self._sons_nums += 1
        newNode.father = self

    def __delete_node(self, index):
        """删除指定位置的子节点，慎用，不会触发B树的修复机制"""
        assert index < self._sons_nums
        self._sons[index:] = self._sons[index+1:]
        self._sons_nums -= 1

    def printKeys(self):
        """打印节点关键字"""
        print('keys: ', end=' ')
        for i in range(self.keys_nums):
            print(self._keys[i], end=' ')
        print('\n')

    def search(self, target):
        """搜索目标关键字，返回索引"""
        return self.__search(target)

    def __search(self, target):
        if self.keys_nums == 0:
            return -1
        # 当关键字数量不大于4的情况下使用顺序查找
        if self.keys_nums <= 4:
            for index in range(self.keys_nums):
                if self._keys[index] == target:
                    return index
            return -1
        # 当关键字数量大于4的情况下使用二分查找
        else:
            left, right = 0, self.keys_nums - 1
            while left <= right:
                mid = (left + right) // 2
                if self._keys[mid] == target:
                    return mid
                elif self._keys[mid] < target:
                    left = mid + 1
                else:
                    right = mid - 1
            return -1

    def search_node(self, target):
        """搜索子节点，返回索引"""
        return self.__search_node(target)

    def __search_node(self, target):
        if self._sons_nums == 0:
            return -1
        index = 0
        while index < self._sons_nums:
            if self._sons[index] == target:
                return index
            index += 1
        return -1

    @property
    def father(self):
        """Get father"""
        return self._father

    @father.setter
    def father(self, newNode):
        """Set father"""
        if newNode:
            assert isinstance(newNode, BNode), 'Mismatched type!'  # 判断阶数是否一致
            self._father = newNode

    @property
    def keys(self):
        return self._keys

    @property
    def keys_nums(self):
        """Get number of keys"""
        return self._keys_nums

    @property
    def sons(self):
        """Get sons"""
        return self._sons

    @property
    def sons_nums(self):
        """Get number of sons"""
        return self._sons_nums


class BTree:
    """B树的实现"""
    def __init__(self, order, sourceCollection=None):
        """
        构造函数。

        :param order: 整型值。大于0，表示B树的阶数
        """
        self._order = order

        self._root = None  # 根节点
        self._node_number = 0  # B树中的节点树

        self._least_key_number_inner = (ceil(self._order / 2) - 1)
        self._least_son_number_inner = ceil(self._order / 2)

        if sourceCollection:
            for item in sourceCollection:
                self.add(item)

    def __len__(self):
        """节点数量"""
        return self._node_number

    def __contains__(self, item):
        """item是否在B树中"""
        return self.find(item) != -1

    def isEmpty(self):
        """B树是否为空"""
        return self._root is None

    def printBTree(self):
        """直观打印二叉树"""
        if not self.root:
            return
        print('=' * 50)
        print('B Tree')
        self.__printInorder(self.root, 0, 17)
        print('=' * 50)

    def __printInorder(self, root, height, length):
        """递归打印二叉树"""
        index = None
        if root.sons_nums:
            index = root.sons_nums - 1
            while (root.sons_nums // 2) <= index:
                self.__printInorder(root.sons[index], height + 1, length)
                index -= 1
        string = 'keys: ' + str(root.keys)
        leftLen = length // 2
        rightLen = length - len(string) - leftLen
        res = " " * leftLen + string + " " * rightLen
        print(" " * height * length + res)
        if root.sons_nums:
            while 0 <= index < (root.sons_nums // 2):
                self.__printInorder(root.sons[index], height + 1, length)
                index -= 1
            print()
            print()

    def add(self, newItem):
        """向B树中添加新关键字"""
        self.__add(newItem)

    def __add(self, newItem):
        if self.isEmpty():
            # 若B树为空，则建立根节点
            self._root = BNode()
            self._root.add_key(newItem)
        else:
            # 若B树不为空，则插入对应的叶子节点，并修复B树
            # 定位到叶子节点
            cursor = self.__find(newItem)
            # 插入新值
            cursor.add_key(newItem)

            # 判断当前节点关键字数量是否超出阶数限制。若超出，则触发节点拆分进行修复，否则不进行任何操作。
            while cursor.keys_nums > self.order - 1:
                self.__split_node(cursor)
                cursor = cursor.father
                if cursor is None:
                    break

    def delete(self, target):
        """删除关键字"""
        self.__delete(target)

    def __delete(self, target):
        # 定位target
        node = self.__find(target, location=True)
        index = node.search(target)
        if index == -1:
            raise ValueNotFound(target)

        # 判断待删值情况

        # 待删关键字不是叶子节点，则与其后继关键字值交换位置后，删除后继关键字
        if node.sons_nums != 0:
            cursor = node.sons[index + 1]
            while cursor.sons_nums:
                cursor = cursor.sons[0]
            node.keys[index], cursor.keys[0] = cursor.keys[0], node.keys[index]  # 交换关键字位置
            node, index = cursor, 0

        # 删除这个关键字
        node.delete_key(node.keys[index])

        # 若待删节点为根节点且关键字为空，则重置B树
        if self.root == node and node.keys_nums == 0:
            self.root = None
            self._node_number = 0
            return

        # 删除后B树的修复
        cursor = node
        while True:
            if self.root == cursor:
                break
            # 若当前节点关键字数量低于下限，则需要修复B树
            if cursor.keys_nums < self._least_key_number_inner:
                me_index = cursor.father.search_node(cursor)  # 当前节点在父节点的子节点中的索引
                # 若存在关键字数量大于下限的兄弟节点，则触发借关键字操作
                if self.__rich_brother(cursor) != -1:
                    brother, brother_index = self.__rich_brother(cursor)  # 可借的兄弟节点及其索引
                    if me_index < brother_index:
                        cursor.add_key(cursor.father.keys[me_index])
                        cursor.father.keys[me_index] = brother.keys[0]
                        brother.delete_key(brother.keys[0])
                    else:
                        cursor.add_key(cursor.father.keys[me_index-1])
                        cursor.father.keys[me_index-1] = brother.keys[-1]
                        brother.delete_key(brother.keys[-1])

                # 否则触发节点合并操作
                else:
                    # 若当前节点索引为0，则与其右侧节点合并
                    if me_index == 0:
                        brother_index = 1
                        brother = cursor.father.sons[brother_index]
                        new_collections = cursor.keys + [cursor.father.keys[0]] + brother.keys
                        new_node = BNode(sourceCollection=new_collections)
                        if cursor.sons_nums or brother.sons_nums:  # 继承子节点
                            for item in cursor.sons[:]:
                                new_node.add_node(item)
                            for item in brother.sons[:]:
                                new_node.add_node(item)
                        cursor.father.delete_key(cursor.father.keys[0])

                        # 这里可能出现BNode.delete_key()方法已经完成了根节点与子节点的合并，造成cursor.father.sons_nums为1的情况
                        if cursor.father.sons_nums == 1:
                            cursor.father.sons[0] = new_node
                        else:
                            cursor.father.sons[1] = new_node
                            cursor.father.sons[:] = cursor.father.sons[1:]

                    # 若当前节点索引不为0，则与其左侧节点合并
                    else:
                        brother_index = me_index - 1
                        brother = cursor.father.sons[brother_index]
                        # 当阶数较低时，这里可能出现cursor.keys_nums为0的情况
                        if cursor.keys_nums:
                            new_collections = brother.keys + [cursor.father.keys[brother_index]] + cursor.keys
                        else:
                            new_collections = brother.keys + [cursor.father.keys[brother_index]]
                        new_node = BNode(sourceCollection=new_collections)
                        if cursor.sons_nums or brother.sons_nums:  # 继承子节点
                            for item in brother.sons[:]:
                                new_node.add_node(item)
                            for item in cursor.sons[:]:
                                new_node.add_node(item)
                        cursor.father.delete_key(cursor.father.keys[brother_index])  # 内部合并子节点
                        cursor.father.sons[brother_index] = new_node
                    if cursor.father.keys_nums == 0:
                        self.root = new_node
                        break
                    else:
                        new_node.father = cursor.father
                cursor = cursor.father
            else:
                break

    def find(self, target):
        """查找关键字，并返回节点和索引"""
        node = self.__find(target, location=True)  # 定位节点
        index = node.search(target)  # 定位索引
        if index == -1:
            return -1  # 未找到
        return node, index

    def __find(self, newItem, location=False):
        """
        返回目标值需要被插入的节点

        :param newItem: 寻找的目标值
        :param location: 布尔值。False用于self.__add()定位叶子节点，True用于self.find()定位目标值所在的节点（不一定是叶子节点）
                      加入这个参数是为了在self.find()中复用self.__find()的代码。
        """
        cursor = self._root
        if not location:
            while cursor.sons_nums:
                if newItem < cursor.keys[0]:
                    cursor = cursor.sons[0]
                elif newItem >= cursor.keys[-1]:
                    cursor = cursor.sons[cursor.sons_nums - 1]
                else:
                    index = 0
                    while cursor.keys[index] <= newItem:
                        index += 1
                    cursor = cursor.sons[index]
        else:
            while cursor.sons_nums:
                index = 0
                while index <= (cursor.keys_nums-1):
                    if cursor.keys[index] == newItem:
                        return cursor
                    if cursor.keys[index] < newItem:
                        index += 1
                    else:
                        break
                cursor = cursor.sons[index]
        return cursor

    def __rich_brother(self, node):
        """返回指定节点的关键字数量大于下限的兄弟节点和其索引，若不存在则返回-1"""
        if self.root == node:
            return -1

        # 定位node在父节点子节点中的索引index
        father = node.father
        index = father.search_node(node)

        # index取到非0值时
        if index != 0 and father.sons[index-1].keys_nums > self._least_key_number_inner:
            return father.sons[index-1], index-1
        # index取到非子节点数量-1时
        elif index != (father.sons_nums - 1) and father.sons[index+1].keys_nums > self._least_key_number_inner:
            return father.sons[index + 1], index + 1
        else:
            return -1

    def __split_node(self, node):
        """节点拆分"""
        father = node.father
        # 提取的关键字的左侧关键字组成新子节点left，右侧关键字组成新子节点right
        ind = node.keys_nums // 2
        left = BNode(sourceCollection=node.keys[:ind])
        right = BNode(sourceCollection=node.keys[ind + 1:])
        # left和right分别继承被提取关键字左侧子节点和右侧子节点
        if node.sons_nums:
            i = 0
            while i <= ind:
                left.add_node(node.sons[i])
                i += 1
            while i < node.sons_nums:
                right.add_node(node.sons[i])
                i += 1
        # 若当前节点为根节点，则将提取的关键字作为新的根节点，并重新分配产生的left和right子节点
        if not father:
            self.root = BNode(sourceCollection=[node.keys[ind]])
            self.root.add_node(left, 0)
            self.root.add_node(right, 1)
        # 若当前节点为非根节点，则将提取的关键字并入父节点，并重新分配产生的left和right子节点
        else:
            insert_pos = father.add_key(node.keys[ind])  # 提取关键字，并入父节点，得到插入位置的索引
            father.add_node(left, insert_pos)
            father.sons[insert_pos+1], right.father = right, father  # 完成子节点的变化

    def __combine_node(self, node):
        pass

    @property
    def order(self):
        return self._order

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, newNode):
        self._root = newNode


class BTreeError(Exception):
    """B树异常的基类"""
    pass


class KeyNumberOverflowError(BTreeError):
    """关键字数量溢出异常"""
    def __init__(self):
        pass

    def __str__(self):
        print("当前节点关键字数量发生溢出！")


class SonNumberOverflowError(BTreeError):
    """子节点数量溢出异常"""
    def __init__(self):
        pass

    def __str__(self):
        print("当前节点子节点数量超出节点阶数")


class ValueNotFound(BTreeError):
    """目标值未找到异常"""
    def __init__(self, item):
        self.item = item

    def __str__(self):
        print('目标值{}不存在！'.format(self.item))


if __name__ == '__main__':
    # BNode测试
    # newNode1 = BNode()
    # newNode1.add_key(3)
    # newNode1.printKeys()
    # newNode1.add_key(5)
    # newNode1.printKeys()
    # newNode1.add_key(4)
    # newNode1.printKeys()
    # print(newNode1.sons_nums)

    # B树测试
    order = 5
    source_collections = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    btree = BTree(order, source_collections)
    btree.printBTree()
    btree.delete(20)
    btree.printBTree()
    btree.delete(19)
    btree.printBTree()
    btree.delete(18)
    btree.printBTree()
