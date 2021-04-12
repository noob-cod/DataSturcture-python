"""
File: tree_bstree_linked.py
Author: Ken Lambert

An implement of Binary Search Tree
二叉搜索树的实现.
"""
from node_bst import BSTNode
from stack_array import ArrayStack


class LinkedBST:

    def __init__(self, sourceCollection=None):
        """Construct a link-based BS-tree(Binary Search Tree), and add items from sourceCollection to it."""
        self._size = 0  # 二叉树节点数
        self._root = BSTNode(None)  # 根节点

        if sourceCollection is not None:
            for item in sourceCollection:
                self.add(item)

    # Mutator
    def isEmpty(self):
        """Return True if self is empty, or False otherwise."""
        return len(self) == 0

    def __len__(self):
        """Return elements number of self."""
        return self._size

    def __str__(self):
        """Returns a string representation with the tree rotated 90 degrees counterclockwise."""

        def recurse(node, level):  # 节点递归函数
            s = ''
            if node is not None:  # 若节点存在
                s += recurse(node.right, level + 1)  # 递归右节点
                s += '| ' * level
                s += str(node.data) + '\n'
                s += recurse(node.left, level + 1)  # 递归左节点
            return s

        return recurse(self._root, 0)

    def __add__(self, other):  # 魔法函数，+
        """Return a new BS-tree containing self and other."""
        result = LinkedBST(self)
        for item in other:
            result.add(item)
        return result

    def clear(self):
        """Make self become emtpy."""
        self._size = 0
        self._root = BSTNode(None)

    def add(self, item):
        """Add item to the tree."""

        def recurse(node):  # 寻找item位置的递归函数
            if item < node.data:  # 若item小于当前节点保存的数据，则搜索左子树。
                if node.left is None:
                    node.left = BSTNode(item)  # 若当前节点无左节点，则直接将item添加为左节点
                else:
                    recurse(node.left)  # 否则继续搜索左子树
            elif node.right is None:
                node.right = BSTNode(item)  # 若当前节点无右节点，则直接将item添加为右节点
            else:
                recurse(node.right)  # 若item不小于当前节点，则搜索右子树
            # End of recurse

        if self.isEmpty():  # 若树为空，则将item添加为根节点
            self._root = BSTNode(item)
        else:  # 若树不为空，则搜索item的位置
            recurse(self._root)
        self._size += 1  # 树的节点数加1

    # Accessor
    def __iter__(self):  # 前序遍历
        """
        Supports an preorder traversal on a view of self.

        If Using recursion implementation, it will cost O(n) complexity both on time and memory. So, we choose to
        implement it with ArrayStack.

        Recursion implementation:
            value_list = []

            def recurse(node):
                if node is not None:
                    value_list.append(node.data)
                    recurse(node.left)
                    recurse(node.right)
            recurse(self._root)
            return iter(value_list)
        """
        node_stack = ArrayStack()  # 创建一个空栈
        node_stack.push(self._root)  # 将根节点压入空栈中
        while not node_stack.isEmpty():  # 当栈不为空
            node = node_stack.pop()  # 弹出栈顶元素
            yield node.data  # 传出栈顶元素数据
            if node.right is not None:  # 若弹出的节点有右节点，则将右节点压入栈中
                node_stack.push(node.right)
            if node.left is not None:  # 若弹出的节点有左节点，则将左节点压入栈中
                node_stack.push(node.left)

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        value_list = []

        def recurse(node):  # 中序遍历递归函数
            if node is not None:
                recurse(node.left)
                value_list.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(value_list)

    def postorder(self):
        """Supports an postorder traversal on a view of self."""
        value_list = []

        def recurse(node):  # 后序遍历递归函数
            if node.left is not None:
                recurse(node.left)
            if node.right is not None:
                recurse(node.right)
            value_list.append(node.data)

        recurse(self._root)
        return iter(value_list)

    def levelorder(self):
        """Supports an levelorder traversal on a view of self."""
        value_list = []

        def recurse(node):  # 层序遍历递归函数
            if node.left is not None:
                value_list.append(node.left.data)
            if node.right is not None:
                value_list.append(node.right.data)
            recurse(node.left)
            recurse(node.right)

        recurse(self._root)
        return iter(value_list)

    def __contains__(self, item):  # 魔法函数，in
        """Return True if item is in self, or False otherwise"""
        return self.find(item) is not None

    def remove(self, item):
        """
        Precondition: The item is in self.
        Raise: Value error if self is emtpy or item is not in self.
        Post-condition: Item is moved out from self
        """
        def backend(node_to_del):  # 辅助删除递归函数
            father_node = node_to_del  # 将父节点设为待删节点
            if father_node.left is not None:  # 若待删节点有左子节点
                node = father_node.left
                if node.right is not None:  # 若待删节点的左子节点有右子节点
                    while node.right is not None:  # 找到待删节点左子树的最右叶子节点
                        father_node = node
                        node = node.right
                    node_to_del.data = node.data  # 用待删节点左子树的最右叶子节点数据覆盖待删数据
                    father_node.right = None  # 删除待删节点左子树的最右叶子节点
                else:  # 若待删节点的左子节点无右子节点，则直接将待删节点的左子节点及其附属子树覆盖待删节点
                    father_node.data = node.data
                    father_node.left = node.left
            else:  # 若待删节点无左子节点，则直接将待删节点的有子节点及其附属子树覆盖待删节点
                # father_node.right = father_node.right.left
                father_node.data = father_node.right.data
                father_node.left = father_node.right.left
                father_node.right = father_node.right.right

        def recurse(root, val):  # 目标节点搜索函数
            """
            node = root
            if node.left.data != val and node.right.data != val:
                recurse(node.left, val)
                recurse(node.right, val)
            else:
                if node.left.data == val:
                    return node, node.left  # 若节点的左子节点数据等于val，则返回该节点及其左子节点
                else:
                    return node, node.right
            """
            node = root
            if node.data == val:
                return node
            elif node.data < val:  # 若val大于node.data
                recurse(node.right, val)
            else:
                recurse(node.left, val)

        root = self._root
        node = recurse(root, item)  # 得到item所在节点与其父节点
        backend(node)  # 删除节点
        self._size -= 1  # 树节点数减1
        self._root = root

    def find(self, item):
        """
        Precondition: Self is not empty.
        Raise: Value error if self is empty.
        Post-condition: Return the item if it is in self, or None if it is not.
        """
        def recurse(node):  # 递归搜索函数
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        # Top-level call on the root node
        return recurse(self._root)

    def replace(self, item, newItem):
        """
        Precondition: Self is not empty and item is in self.
        Raise: Value error if self is empty or item is not in self.
        Post-condition: The item is replaced by the newItem.
        """
        def recurse(node, replaced=False):  # 迭代搜索替换函数
            if item == node.data:
                node.data = newItem
                replaced = True  # 若替换发生，则说明找到了item，将replaced置位为True
                return replaced
            elif item < node.data:
                recurse(node.left)
            elif item > node.data:
                recurse(node.right)

        if self.isEmpty():
            raise ValueError('Tree is empty!')
        is_replaced = recurse(self._root)  # 搜索替换
        if is_replaced:
            print('%s不在当前树中，替换操作未发生' % str(item))


