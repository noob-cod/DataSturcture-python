"""
@Date: 2021/6/19 下午6:38
@Author: Chen Zhang
@Brief: Implement of BlackRedTree

红黑树数据结构概述：
    1、红黑树简介：
        红黑树是一种自平衡的二叉搜索树，它确保没有一条路径会比其他路径长出两倍，也是4阶B树的特殊实现形式。

    2、红黑树特点
        （1）没和节点要么是红色的，要么是黑色的；
            （黑色节点可以理解为2节点，
             带有一个红色子节点的黑节点可以与其子节点共同视为一个3节点，
             带有两个红色子节点的黑节点可以与其子节点共同视为一个4节点）
        （2）根节点始终是黑色的；
        （3）每个叶子节点（树尾端默认存在的NULL节点）都是黑色的；
        （4）不存在两个相邻的红节点；
        （5）对于任意节点，其到树尾端的NULL节点的每条路径都包含相同数目的黑节点。
        ps:特点（4）和特点（5）共通保证了红黑树中没有一条路径会比其他路径长出两倍

    3、红黑树修复常用操作：
        （1）颜色转变；
        （2）子树旋转
"""


class RBNode:

    def __init__(self, value, left=None, right=None, father=None, color=0):
        """
        红黑节点对象构造函数
        :param left: BRNode, 左子节点。默认为空。
        :param right: BRNode, 右子节点。默认为空。
        :param father: BRNode，父节点。默认为空。
        :param color: 0或1。0代表红色，1代表黑色。默认为红色。
        """
        if left:
            assert isinstance(left, RBNode)
        if right:
            assert isinstance(right, RBNode)
        if father:
            assert isinstance(father, RBNode)
        if color:
            assert (color == 0 or color == 1)
        self.__value = value
        self.__left = left
        self.__right = right
        self.__father = father
        self.__color = color

    @property
    def val(self):
        return self.__value

    @val.setter
    def val(self, value):
        self.__value = value

    @property
    def left(self):
        return self.__left

    @left.setter
    def left(self, node):
        if node is not None:
            assert isinstance(node, RBNode)
        self.__left = node

    @property
    def right(self):
        return self.__right

    @right.setter
    def right(self, node):
        if node is not None:
            assert isinstance(node, RBNode)
        self.__right = node

    @property
    def father(self):
        return self.__father

    @father.setter
    def father(self, node):
        if node:
            assert isinstance(node, RBNode)
        self.__father = node

    @property
    def color(self):
        return self.__color

    def change_color(self):
        self.__color = 1 - self.__color


class RBTree:

    def __init__(self, sourceCollection=None):
        """
        红黑树构造
        :param sourceCollection: 初始参数集，默认为空
        """
        self.__root = RBNode('head', color=1)  # 在根节点前面加一个黑色的head节点，为了在根节点发生旋转时不丢失对根节点的引用
        self.__size = 0

        if sourceCollection:
            assert isinstance(sourceCollection, list)
            for item in sourceCollection:
                self.add(item)

    def printTree(self):
        """直观打印二叉树"""
        if not self.root.left:
            return
        print('=' * 50)
        print('Red Black Tree')
        self.__printInorder(self.root.left, 0, 'H', 17)
        print('=' * 50)

    def __printInorder(self, root, height, preStr, length):
        """递归打印二叉树"""
        if not root:
            return
        self.__printInorder(root.right, height + 1, 'V', length)
        if root.color == 0:
            color = 'r'
        else:
            color = 'b'
        string = preStr + str(root.val) + '(' + color + ')' + preStr
        leftLen = (length - len(string)) // 2
        rightLen = length - len(string) - leftLen
        res = " " * leftLen + string + " " * rightLen
        print(" " * height * length + res)
        self.__printInorder(root.left, height + 1, '^', length)

    def __iter__(self):
        """中序遍历"""
        def recurse(node):
            if node.left:
                recurse(node.left)
            yield node
            if node.right:
                recurse(node.right)

        if self.root.left:
            recurse(self.root.left)

    def __contains__(self, item):
        return not (self.find(item) == -1)

    def find(self, item):
        if self.root.left is None:
            pass
        else:
            cursor = self.root.left
            assert isinstance(item, type(cursor.val)), 'Different type!'
            while True:
                if item == cursor.val:
                    return cursor
                elif item < cursor.val:
                    if cursor.left:
                        cursor = cursor.left
                    else:
                        return -1
                else:
                    if cursor.right:
                        cursor = cursor.right
                    else:
                        return -1

    def add(self, newValue):
        """
        红黑树插入：
            每个新插入的节点都是红色。
            （1）若插入后的新节点为根节点，则将节点标记为黑色
            （2）若插入后的新节点的父节点不是黑色：
                1）若新插入节点的叔叔节点为红色：
                    I.将新插入节点的父节点和其叔叔节点标记为黑色
                    II.将新插入节点的祖父节点标记为红色
                    III.将新插入节点的颜色与其祖父节点颜色相同，对整个树重复II和III

                2）若新插入节点的叔叔节点为黑色：
                    I.左左（新插入节点与其父节点均为左子节点）
                        i.以新插入节点的父节点为基准，右旋（顺时针）以新插入节点的祖父节点为根节点的子树
                        ii.将新插入节点的原父节点变为黑色，原祖父节点变为红色

                    II.左右（新插入节点为右子节点，其父节点为左子节点）
                        i.以新插入节点为基准，左旋（逆时针）以新插入节点的父节点为根节点的子树
                        ii.再应用左左的情况

                    III.右右（新插入节点与其父节点均为右子节点）
                        i.以新插入节点的父节点为基准，左旋（逆时针）以新插入节点的祖父节点为根节点的子树
                        ii.将新插入节点的原父节点变为黑色，原祖父节点变为红色

                    IV.右左（新插入节点为左子节点，其父节点为右子节点）
                        i.以新插入节点为基准，右旋（顺时针）以新插入节点的父节点为根节点的子树
                        ii.再应用右右的情况

        :param newValue: RBNode，新插入的值
        """
        # 构造红黑树节点
        newNode = RBNode(newValue)

        # 红黑树为空
        if not self.root.left:
            self.root.left = newNode
            self.root.left.father = self.root
        # 红黑树不为空
        else:
            cursor = self.root.left  # 辅助指针
            # 插入操作
            while True:
                if cursor.val >= newNode.val:  # 搜索左子树
                    if not cursor.left:
                        cursor.left = newNode
                        newNode.father = cursor
                        cursor = cursor.left
                        break
                    cursor = cursor.left
                else:
                    if not cursor.right:
                        cursor.right = newNode
                        newNode.father = cursor
                        cursor = cursor.right
                        break
                    cursor = cursor.right
            # 修复操作
            while cursor.father != self.root and cursor.father.father != self.root:  # 修复节点不是根节点，也不是根节点的子节点
                self.AddReBalance(cursor)
                cursor = cursor.father
            if self.root.left.color == 0:
                self.root.left.change_color()
        self.__size += 1

    def delete(self, value):
        """
        红黑树删除：
            （1）被删除节点无子节点时：
                1） 若被删除节点是红色，则直接删除即可，不会影响黑色节点数量；
                2） 若被删除节点是黑色，则删除后需要分为9种情况进行修复：
                    父亲为红色：
                    情况1 父亲为红色，兄弟为黑色且有两个子节点
                        - 左旋父节点
                        - 将父节点、兄弟节点、兄弟的右子节点变色
                    情况2 父亲为红色，兄弟为黑色且只有一个左子节点
                        - 右旋兄弟节点
                        - 将兄弟节点与兄弟的左子节点变色
                        - 左旋父节点
                    情况3 父亲为红色，兄弟为黑色且只有一个右子节点
                        - 左旋父节点
                    情况4 父亲为红色，兄弟为黑色且没有子节点
                        - 将父亲节点与兄弟节点变色。

                    父亲为黑色：
                    情况5 父亲为黑色，兄弟为红色且有两个黑色子节点
                        - 左旋父节点
                        - 将兄弟节点与兄弟节点的左子节点变色
                    情况6 父亲为黑色，兄弟为黑色且有两个子节点
                        - 左旋父节点
                        - 将兄弟节点的右子节点变色
                    情况7 父亲为黑色，兄弟为黑色且只有一个左子节点
                        - 右旋兄弟节点
                        - 左旋父节点
                        - 将兄弟节点的左子节点变色
                    情况8 父亲为黑色，兄弟为黑色且只有一个右子节点
                        - 左旋父节点
                        - 将兄弟节点的右子节点变色
                    情况9 父亲为黑色，兄弟为黑色且没有子节点
                        - 将兄弟节点、父节点的兄弟节点变色

            （2）被删除节点有一个子节点时：
                将被删节点与其子节点的值互换，转化为删除其子节点，即没有子节点的节点的情况

            （3）被删除节点有两个子节点时：
                将被删节点与其后继节点的值互换，转化为删除其后继节点，即只有一个子节点或没有子节点的情况

        :param value: 待删的值
        :return:
        """
        node = self.find(value)
        if node == -1:
            raise ValueError('Not Found!')

        # 待删节点有两个子节点，则与后继节点互换值，并取后继节点为新的待删节点
        if node.left and node.right:
            cursor = node.right
            while cursor.left:
                cursor = cursor.left
            node.val, cursor.val = cursor.val, node.val
            node = cursor

        # 待删节点有一个子节点，则与子节点互换值，并取子节点为新的待删节点
        if node.left or node.right:
            if node.left:
                node.val, node.left.val = node.left.val, node.val
                node = node.left
            else:
                node.val, node.right.val = node.right.val, node.val
                node = node.right

        # 待删节点无子节点
        # 若为根节点，则直接释放
        if node == self.root.left:
            self.root.left.father = None
            self.root.left = None

        # 若待删除节点为红色，则直接删除
        elif node.color == 0:
            if node == node.father.left:
                node.father.left = node.father = None
            else:
                node.father.right = node.father = None

        # 若待删除节点为黑色
        else:
            target = RBTools(node)  # 搭建工作平台

            # 直接删除待删节点
            if target.me == target.father.left:
                target.me.father = target.father.left = None
            else:
                target.me.father = target.father.right = None

            # 父节点为红色
            if target.father.color == 0:
                # 情况1：父红，兄黑，兄双子（红）
                if target.brother is not None and target.brother.left and target.brother.right:
                    father_target = RBTools(target.father)
                    father_target.rotate_l()
                    target.father.change_color()
                    target.brother.change_color()
                    target.brother.right.change_color()
                elif target.brother is not None and (target.brother.left or target.brother.right):
                    # 情况2：父红，兄黑，兄左子红
                    if target.brother.left:
                        brother_target = RBTools(target.brother)
                        brother_target.rotate_r()
                        target.brother.change_color()
                        target.brother.father.change_color()  # 原兄弟节点的左子节点变色
                        father_target = RBTools(target.father)
                        father_target.rotate_l()
                    # 情况3：父红，兄黑，兄右子红
                    else:
                        father_target = RBTools(target.father)
                        father_target.rotate_l()
                # 情况4：父红，兄黑，兄无子
                else:
                    target.father.change_color()
                    target.brother.change_color()
            # 父节点为黑色
            else:
                # 情况5：父黑，兄红（兄双子黑）
                if target.brother and target.brother.color == 0:
                    father_target = RBTools(target.father)
                    father_target.rotate_l()
                    target.brother.change_color()
                    target.father.right.change_color()
                # 情况6：父黑，兄黑，兄双子（红）
                elif target.brother and target.brother.color == 1 and target.brother.left and target.brother.right:
                    father_target = RBTools(target.father)
                    father_target.rotate_l()
                    target.brother.right.change_color()
                elif target.brother and target.brother.color == 1 and (target.brother.left or target.brother.right):
                    # 情况7：父黑，兄黑，兄左子（红）
                    if target.brother.left:
                        brother_target = RBTools(target.brother)
                        brother_target.rotate_r()
                        father_target = RBTools(target.father)
                        father_target.rotate_l()
                        target.father.father.change_color()
                    # 情况8：父黑，兄黑，兄右子（红）
                    else:
                        father_target = RBTools(target.father)
                        father_target.rotate_l()
                        target.brother.right.change_color()
                # 情况9：父黑，兄黑，兄无子
                else:
                    target.brother.change_color()
                    # 父亲的兄弟节点变色
                    if target.father == target.grandfather.left and target.grandfather.right:
                        target.grandfather.right.change_color()
                    elif target.father == target.grandfather.right and target.grandfather.left:
                        target.grandfather.left.change_color()
                    else:
                        pass

        self.__size -= 1

    @property
    def root(self):
        return self.__root

    @root.setter
    def root(self, node):
        assert isinstance(node, RBNode)
        self.__root.left = node
        node.father = self.__root.left

    @property
    def size(self):
        return self.__size

    @classmethod
    def AddReBalance(cls, base_node):
        """添加元素后的修复操作"""
        target = RBTools(base_node)  # 搭建工作平台

        if target.me.color == 0 and target.father.color == 0:

            # 叔叔节点为黑色
            if target.uncle is None or target.uncle.color == 1:
                # 左左
                if target.father == target.grandfather.left and target.me == target.father.left:
                    # 以祖父节点为基准右旋
                    grandfather_target = RBTools(target.grandfather)
                    grandfather_target.rotate_r()
                    # 右旋后插入节点、原父节点，原祖父节点变色
                    # target.me.change_color()
                    target.father.change_color()
                    target.grandfather.change_color()

                # 左右
                elif target.me.father == target.grandfather.left and target.me == target.me.father.right:
                    # 以父节点为基准左旋，再以原祖父节点为基准右旋
                    father_target = RBTools(target.father)
                    father_target.rotate_l()
                    grandfather_target = RBTools(target.grandfather)
                    grandfather_target.rotate_r()
                    # 原插入节点与原祖父节点变色
                    target.me.change_color()
                    target.grandfather.change_color()

                # 右右
                elif target.me.father == target.grandfather.right and target.me == target.me.father.right:
                    # 以祖父节点为基准左旋
                    grandfather_target = RBTools(target.grandfather)
                    grandfather_target.rotate_l()
                    # 左旋后插入节点、原父节点、原祖父节点变色
                    # target.me.change_color()
                    target.father.change_color()
                    target.grandfather.change_color()

                # 右左
                else:
                    # 以父节点为基准右旋，再以原祖父节点为基准左旋
                    father_target = RBTools(target.father)
                    father_target.rotate_r()
                    grandfather_target = RBTools(target.grandfather)
                    grandfather_target.rotate_l()
                    # 原插入节点与原祖父节点变色
                    target.me.change_color()
                    target.grandfather.change_color()

            # 叔叔节点为红色
            else:
                # self.ColorReBalance(target.me)

                # 父节点，叔叔节点，祖父节点变色
                target.father.change_color()
                if target.uncle:
                    target.uncle.change_color()
                if target.grandfather:
                    target.grandfather.change_color()

        # 节点与其父节点不同时为红色
        else:
            pass


class RBTools:

    def __init__(self, cur_node):
        """构造一个以传入节点为目标的工作平台，提供对目标节点的祖父节点、兄弟节点、叔叔节点的快速引用"""
        assert isinstance(cur_node, RBNode)
        self.__cur_node = cur_node

        self.__father = None
        self.__grandfather = None
        self.__brother = None
        self.__uncle = None

        if self.__cur_node.father:
            self.__father = self.__cur_node.father
            if self.__cur_node == self.__cur_node.father.left:
                self.__brother = self.__cur_node.father.right
            else:
                self.__brother = self.__cur_node.father.left

            if self.__cur_node.father.father:
                self.__grandfather = self.__cur_node.father.father
                if self.__cur_node.father == self.__grandfather.left:
                    self.__uncle = self.__grandfather.right
                else:
                    self.__uncle = self.__grandfather.left

    @property
    def me(self):
        return self.__cur_node

    @property
    def father(self):
        return self.__father

    @father.setter
    def father(self, newVal):
        self.__father = newVal

    @property
    def grandfather(self):
        return self.__grandfather

    @property
    def brother(self):
        return self.__brother

    @property
    def uncle(self):
        return self.__uncle

    def rotate_l(self):
        """左旋操作"""
        if not self.me.right:
            raise TypeError('必须拥有右子树才可以进行左旋操作!')

        # 若目标存在父节点，则先转移父节点归属
        if self.me.father:
            father = self.me.father
            if self.me == self.me.father.left:
                father.left = self.me.right
            else:
                father.right = self.me.right
            self.me.right.father = father

        tmp = None
        if self.me.right.left:
            tmp = self.me.right.left
        self.me.father = self.me.right
        self.me.father.left = self.me
        self.me.right = tmp
        if tmp:
            tmp.father = self.me

    def rotate_r(self):
        """右旋操作"""
        if not self.me.left:
            raise TypeError('必须拥有左子树才可以进行右旋操作!')

        # 若目标存在父节点，则先转移父节点归属
        if self.me.father:
            father = self.me.father
            if self.me == self.me.father.left:
                father.left = self.me.left
            else:
                father.right = self.me.left
            self.me.left.father = father

        tmp = None
        if self.me.left.right:
            tmp = self.me.left.right
        self.me.father = self.me.left
        self.me.father.right = self.me
        self.me.left = None
        self.me.left = tmp
        if tmp:
            tmp.father = self.me


if __name__ == '__main__':
    samples = [1, 2, 3, 4, 5, 6, 7, 8]
    RedBlackTree = RBTree(samples)
    RedBlackTree.printTree()
    print()

    # 删除操作平衡性检测
    RedBlackTree.delete(1)
    RedBlackTree.printTree()
    print()
    RedBlackTree.delete(2)
    RedBlackTree.printTree()
    print()
    RedBlackTree.delete(3)
    RedBlackTree.printTree()
    print()
    RedBlackTree.delete(100)
