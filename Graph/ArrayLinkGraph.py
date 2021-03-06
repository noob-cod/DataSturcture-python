"""
@Date: 2021/4/2 下午9:19
@Author: Chen Zhang
@Brief: 基于链表的图的实现
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath('ArrayLinkGraph.py'))))


class ArrayLinkGraph:
    """The implement of linked-list-based graph"""
    def __init__(self, num_of_nods, edges_list, directed=False, weighted=False):
        """
        Create a new graph and save all information in a linked list.

        :param num_of_nods: The amount of nodes
        :param edges_list: A list describes edges of graph, [(node_i, node_j), ...]
        :param directed: Bool, if True create directed graph, else create undirected graph.
        :param weighted: Bool, if True save edge weight, else not.
        """
        self.node_num = num_of_nods  # number of nodes
        self.edge_num = len(edges_list)  # number of edges
        self.directed = directed  # directed or not
        self.weighted = weighted  # weighted or not
        self.llist = OnewayLinkedlist()  # graph
        self.node_name_dict = {}  # save name of nodes

    def __len__(self):
        pass

    def __str__(self):
        return ''

    def add_edge(self, newEdge):
        pass

    def del_edge(self, edge):
        pass


if __name__ == '__main__':
    pass
