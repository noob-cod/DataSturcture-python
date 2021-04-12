"""
File: node_bst.py
Author: Kim Lambert

二叉搜索树的节点类
"""


class BSTNode:

    def __init__(self, data, left=None, right=None):
        """Instantiate a BST node with default left and right of None."""
        self.data = data  # 数据
        self.left = left  # 左节点
        self.right = right  # 右节点
