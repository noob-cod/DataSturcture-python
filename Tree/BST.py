"""
@Date: Sunday, March 28, 2021
@Author: Chen Zhang
@Brief: 红黑树的实现

红黑树数据结构概述：
    1、红黑树与二叉搜索树的关系：
        红黑树的本质是一个二叉搜索树，但红黑树是自平衡的。
        传统的二叉搜索树在建立的过程中受到元素插入顺序的影响，可能会产生不平衡的现象，进而导致二叉树退化，影响效率。
        红黑树通过引入调节机制，使得二叉搜索树在构建的过程中尽可能的保持平衡。

    2、红黑树机制：
        规则：
            （1）每个节点都有红色或黑色；
            （2）树的根节点始终为黑色；
            （3）没有两个相邻的红色节点；
            （4）从节点（包括根节点）到其任何后代NULL节点（叶子节点下方挂的两个空节点，并且认为它们是黑色）的每条路径
                都具有相同数量的黑色节点；

        特殊机制：
            （1）颜色转换：特殊情况下改变节点的颜色；
            （2）节点旋转

        新节点插入：
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

        删除已有节点：
            （1）被删除节点无子节点时：
                a. 若被删除节点是红色，则直接删除即可，不会影响黑色节点数量；
                b. 若被删除节点是黑色，则删除后需要进行平衡操作；

            （2）被删除节点有一个子节点时：
                将被删除节点的子节点接到被删除节点的父节点上，并将子节点颜色涂黑，保证黑色节点数量。

            （3）被删除节点有两个子节点时：
                使用后继节点作为替换的删除节点，转化为（1）或（2）中的情况进行处理。

            被删节点为黑色时删除后的平衡操作
            1. 被删节点为根节点时
                无需进行平衡操作

            2. 兄弟节点为黑色时
                2.1 兄弟节点的子节点全为黑色
                    2.1.1 被删节点的父节点为红色
                        交换父节点与兄弟节点的颜色

                    2.1.2 被删节点的父节点为黑色
                        将兄弟节点涂红；令父节点为新的待删节点，递归处理。

                2.2 兄弟节点的子节点不全是黑色
                    2.2.1 兄弟节点为左子节点，兄弟节点的左子节点为红色
                        交换父节点与兄弟节点的颜色，将兄弟节点的左子节点涂黑，右旋父节点

                    2.2.2 兄弟节点为右子节点，兄弟节点的右子节点为红色
                        交换父节点与兄弟节点的颜色，将兄弟节点的右子节点涂黑，左旋父节点

                    2.2.3 兄弟节点为左子节点，兄弟节点的左子节点为黑色
                        交换兄弟节点与兄弟节点的右子节点的颜色，左旋兄弟节点，转换至2.2.1

                    2.2.4 兄弟节点为右子节点，兄弟节点的右子节点为黑色
                        交换兄弟节点与兄弟节点的左子节点的颜色，右旋兄弟节点，转换至2.2.2

            3. 兄弟节点为红色时
                3.1 兄弟节点为左子节点
                    交换父节点与兄弟节点的颜色，右旋父节点，转化为情形2

                3.2 兄弟节点为右子节点
                    交换父节点与兄弟节点的颜色，左旋父节点，转化为情形2
"""


class RBTNode:
    def __init__(self, data, left=None, right=None, color=0, father=None):
        self.data = data
        self.left = left
        self.right = right

        self.color = color  # 节点的颜色，0为黑色，1为红色
        self.father = father  # 父节点，默认为空


class RBT:
    """Implement of Red-Black Tree"""
    def __init__(self, sourceCollection=None):
        """构造红黑树"""
        self.root = None  # 根节点
        self._num = 0  # 树的节点数
        if sourceCollection:
            for item in sourceCollection:
                self.add(item)
                self._num += 1

    def __len__(self):
        """返回树中的节点数"""
        return self._num

    def add(self, newItem):
        """向树中添加新的值"""
        # 当树为空时，插入为根节点
        if self.root is None:
            self.root = RBTNode(newItem, RBTNode(None), RBTNode(None))  # 默认为黑色
        # 当树不为空时
        else:
            def recurse(node, value):
                """递归插入新的节点"""
                if value <= node.data:  # 若value小于节点中数据，则搜索左子树
                    if node.left.data is None:  # 若左子树为空
                        node.left = RBTNode(value, RBTNode(None), RBTNode(None), color=1, father=node)  # 插入
                        return node.left
                    else:
                        newNode = recurse(node.left, value)  # 搜索
                        return newNode
                else:  # 若value大于节点中数据，则搜索右子树
                    if node.right.data is None:  # 若右子树为空
                        node.right = RBTNode(value, RBTNode(None), RBTNode(None), color=1, father=node)  # 插入
                        return node.right
                    else:
                        newNode = recurse(node.right, value)  # 搜索
                        return newNode

            # 完成新节点的插入
            new_node = recurse(self.root, newItem)

            # 递归维护红黑树
            while new_node.father != self.root and new_node != self.root:  # 若父节点不是根节点
                if not (new_node.father.color == 1 and new_node.color == 1):  # 若新节点与父节点都是红色
                    break
                else:
                    if new_node.father.father.left.color == 1 and new_node.father.father.right.color == 1:  # 若叔叔节点为红色
                        new_node.father.father.left.color = 0  # 将叔叔节点（父节点）变为黑色
                        new_node.father.father.right.color = 0  # 将父节点（叔叔节点）变为黑色
                        new_node.father.father.color = 1  # 将祖父节点变为红色
                        new_node = new_node.father.father  # 递归至祖父节点
                    else:
                        temp = None  # 存放曾祖父节点
                        if new_node == new_node.father.left and new_node.father == new_node.father.father.left:  # 左左
                            if new_node.father.father.father:  # 若祖父节点不是根节点
                                temp = new_node.father.father.father  # 记录曾祖父节点
                            new_root = RBT.right_rotate(new_node.father.father)  # 右旋父节点
                            new_root.color = 0  # 原父节点变为黑色
                            new_root.right.color = 1  # 原祖父节点变为红色
                            if temp:
                                if temp.left == new_root.right:
                                    temp.left = new_root
                                else:
                                    temp.right = new_root
                                new_root.father = temp
                            else:  # 若原祖父节点为根节点，则将self.root指向新的根节点
                                new_root.father = None
                                self.root = new_root
                        elif new_node == new_node.father.right and new_node.father == new_node.father.father.left:  # 左右
                            # 左旋新插入节点
                            temp = new_node.father.father
                            new_root_ = RBT.left_rotate(new_node.father)
                            if temp.left == new_root_.left:
                                temp.left = new_root_
                            else:
                                temp.right = new_root_
                            new_root_.father = temp
                            # 重置temp
                            temp = None
                            # 应用左左的情况
                            if new_node.father.father.father:  # 若存在曾祖父节点
                                temp = new_node.father.father.father  # 记录曾祖父节点
                            new_root = RBT.right_rotate(new_node.father.father)
                            new_root.color = 0  # 原父节点变为黑色
                            new_root.right.color = 1  # 原祖父节点变为红色
                            if temp:
                                if temp.left == new_root.right:
                                    temp.left = new_root
                                else:
                                    temp.right = new_root
                                new_root.father = temp
                            else:  # 若原祖父节点为根节点，则将self.root指向新的根节点
                                new_root.father = None
                                self.root = new_root
                        elif new_node == new_node.father.right and new_node.father == new_node.father.father.right:  # 右右
                            if new_node.father.father.father:  # 若存在曾祖父节点
                                temp = new_node.father.father.father  # 记录曾祖父节点
                            new_root = RBT.left_rotate(new_node.father.father)
                            new_root.color = 0  # 原父节点变为黑色
                            new_root.left.color = 1  # 原祖父节点变为红色
                            if temp:  # 若原祖父节点为根节点，则将self.root指向新的根节点
                                if temp.left == new_root.right:
                                    temp.left = new_root
                                else:
                                    temp.right = new_root
                                new_root.father = temp
                            else:
                                new_root.father = None
                                self.root = new_root
                        else:  # 右左
                            # 右旋新插入节点
                            temp = new_node.father.father
                            new_root_ = RBT.right_rotate(new_node.father)
                            if temp.left == new_root_.left:
                                temp.left = new_root_
                            else:
                                temp.right = new_root_
                            new_root_.father = temp
                            # 重置temp
                            temp = None
                            # 再应用右右的情况
                            if new_node.father.father.father:  # 若存在曾祖父节点
                                temp = new_node.father.father.father  # 记录曾祖父节点
                            new_root = RBT.left_rotate(new_node.father.father)
                            new_root.color = 0  # 原父节点变为黑色
                            new_root.left.color = 1  # 原祖父节点变为红色
                            if temp:  # 若原祖父节点为根节点，则将self.root指向新的根节点
                                if temp.left == new_root.right:
                                    temp.left = new_root
                                else:
                                    temp.right = new_root
                                new_root.father = temp
                            else:
                                new_root.father = None
                                self.root = new_root
                        new_node = new_node.father  # 递归
            self.root.color = 0  # 根节点置为黑色

    def delete(self, value):
        """删除指定元素，红黑树中被删除元素和后继元素只是互换数值，颜色不会互换"""
        # 定位元素的位置
        def recurse(node, target):
            if node.data is None:  # 未找到
                return -1
            if target == node.data:
                return node
            elif target <= node.data:
                res = recurse(node.left, target)
                return res
            else:
                res = recurse(node.right, target)
                return res
        t_node = recurse(self.root, value)  # 找到要删除的节点

        # 按二叉树删除原则删除目标节点
        if t_node.left.data is not None and t_node.right.data is not None:  # 若待删除节点有两个子节点
            f_node = t_node.father
            if f_node.left == t_node:  # 待删节点是左子节点，则用其左子树的最右节点替换待删节点
                # 寻找待删节点左子树的最右节点，并删除
                cursor_lr = t_node.left
                while cursor_lr.right.data is not None:
                    cursor_lr = cursor_lr.right
                temp_value = cursor_lr.data  # 保存左子树最右节点的值
                cursor_lr.father.right = RBTNode(None)  # 删除该最右节点
                # 替换待删节点的值，完成删除操作
                t_node.data = temp_value
            else:  # 待删节点是右子节点，则用其右子树的最左节点替换待删节点
                # 寻找待删节点右子树的最左节点，并删除
                cursor_rl = t_node.right
                while cursor_rl.left.data is not None:
                    cursor_rl = cursor_rl.left
                temp_value = cursor_rl.data  # 保存右子树最左节点的值
                cursor_rl.father.left = RBTNode(None)  # 删除该最左节点
                # 替换待删节点的值，完成删除操作
                t_node.data = cursor_rl
        else:
            if t_node.left.data is None and t_node.right.data is None:  # 若待删除节点无子节点，则直接删除
                f_node = t_node.father
                if f_node.left == t_node:  # 待删节点是左子节点
                    f_node.left = RBTNode(None)
                else:  # 待删节点是右子节点
                    f_node.right = RBTNode(None)
            else:  # 若待删除节点有一个子节点
                if t_node.left.data is None:  # 若待删除节点无左子树，则用其右子节点替代待删除节点
                    f_node = t_node.father
                    if f_node.left == t_node:  # 待删节点是左子节点
                        f_node.left = t_node.right
                        f_node.left.father = f_node
                    else:  # 待删节点是右子节点
                        f_node.right = t_node.right
                        f_node.right.father = f_node
                else:  # 若待删除节点无右子树，则用其左子节点代替待删除节点
                    f_node = t_node.father
                    if f_node.left == t_node:  # 待删节点是左子节点
                        f_node.left = t_node.left
                        f_node.left.father = f_node
                    else:  # 待删节点是右子节点
                        f_node.right = t_node.left
                        f_node.right.father = f_node

        # 修复红黑树
        # 若删除的是红色节点，则直接删除，不影响红黑树的性质

        # 若删除的是黑色节点则黑高平衡被破坏，需要分情况讨论修复

        # 若被删除节点位置的替代节点X的兄弟节点W为黑色，且其子节点都是黑色

        # 若被删除节点位置的替代节点X的兄弟节点W为黑色，且其右子节点为红色

        # 若被删除节点位置的替代节点X的兄弟节点W为黑色，且子节点左红右黑

        # 若被删除节点位置的替代节点X的兄弟节点W为红色

    @classmethod
    def left_rotate(cls, root):
        """实现对子树根节点的右子节点的左旋操作"""
        p1 = root  # 根节点
        p2 = root.right  # 右子节点
        p1.right = p2.left  # 打断根节点与右子节点的连接，将右子节点的左子树转移到根节点的右子树位置
        p2.left.father = p1
        p2.left = p1  # 将原右子节点的左子节点设为原根节点，完成对右子节点的左旋操作
        p1.father = p2
        return p2  # 返回新的根节点

    @classmethod
    def right_rotate(cls, root):
        """实现对子树根节点的左子节点的右旋操作"""
        p1 = root  # 根节点
        p2 = root.left  # 左子节点
        p1.left = p2.right  # 打断根节点与左子节点的连接，将左子节点的右子树转移到根节点的左子树位置
        p2.right.father = p1
        p2.right = p1  # 将原左子节点的右子节点设为原根节点，完成对左子节点的右旋操作
        p1.father = p2
        return p2  # 返回新的根节点


if __name__ == '__main__':
    tree = RBT([1, 2, 3, 4, 5, 6, 7, 8])
    print(len(tree))
