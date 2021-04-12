"""
@Date: Friday, April 2, 2021
@Author: Chen Zhang
@Brief: 基于邻接矩阵的图的实现
"""


class MatrixGraph:
    """Implement of matrix-based graph"""
    def __init__(self, num_of_nods, edges_list, directed=False, weighted=False):
        """
        Create a new graph

        The graph is formed as:

                n0  n1  n2  n3  n4          Graph=
            n0  0   0   0   0   0            [[0, 0, 0, 0, 0],
            n1  0   0   0   0   0             [0, 0, 0, 0, 0],
            n2  0   0   0   0   0    >>>>>    [0, 0, 0, 0, 0],
            n3  0   0   0   0   0             [0, 0, 0, 0, 0],
            n4  0   0   0   0   0             [0, 0, 0, 0, 0]]

            ni indicates the i_th node of the graph, the value stored in (ni, nj) indicates whether
            there is an edge sourced from node_i and pointed to node_j.

        :param num_of_nods: The amount of nodes
        :param edges_list: A list describes edges of graph, [(node_i, node_j), ...]
        :param directed: Bool, if True create directed graph, else create undirected graph.
        :param weighted: Bool, if True save edge weight, else not.
        """
        assert isinstance(num_of_nods, int), 'Only accept integer!'
        assert len(edges_list) != 0, 'Graph can not be empty!'
        assert isinstance(directed, bool), 'Only accept bool!'
        assert isinstance(weighted, bool), 'Only accept bool!'

        self.node_num = num_of_nods  # number of nodes
        self.edge_num = len(edges_list)  # number of edges
        self.directed = directed  # directed or not
        self.weighted = weighted  # weighted or not
        self.mat = [[0] * self.node_num for _ in range(self.node_num)]  # create empty mat
        self.node_name_dict = {}  # save name of nodes

        # Record edges
        for i in range(self.edge_num):

            # Transfer node name to specific index
            if edges_list[i][0] not in self.node_name_dict:
                self.node_name_dict[edges_list[i][0]] = len(self.node_name_dict)  # 以加入字典的顺序为索引
            if edges_list[i][1] not in self.node_name_dict:
                self.node_name_dict[edges_list[i][1]] = len(self.node_name_dict)

            # Record value of every position
            if self.weighted:  # 记录权值
                self.mat[self.node_name_dict[edges_list[i][0]]][self.node_name_dict[edges_list[i][1]]] = edges_list[i][2]  # 记录edge
                if not self.directed:  # 若为无向图，则将对称位置也置1
                    self.mat[self.node_name_dict[edges_list[i][1]]][self.node_name_dict[edges_list[i][0]]] = edges_list[i][2]
            else:  # 仅标记
                self.mat[self.node_name_dict[edges_list[i][0]]][self.node_name_dict[edges_list[i][1]]] = 1
                if not self.directed:  # 若为无向图，则将对称位置也置1
                    self.mat[self.node_name_dict[edges_list[i][1]]][self.node_name_dict[edges_list[i][0]]] = 1

    def __len__(self):
        """Return (node amount, edge amount)"""
        return self.node_num, self.edge_num

    def __str__(self):
        """Print the graph as a matrix with title"""
        title = sorted(self.node_name_dict.items(), key=lambda x: x[1])
        string = ' ' * (len(str(title[1][0])) + 1)  # Title line
        for i in range(len(title)):
            string += str(title[i][0]) + ' '
        for i in range(self.node_num):
            string += '\n' + str(title[i][0]) + ' ' + ' '.join(map(str, self.mat[i]))
        return string + '\n'

    def add_newEdges(self, newEdge):
        """Add new edges to self"""
        # Check the format of input
        assert isinstance(newEdge, tuple), 'Only accept tuple'
        if self.weighted:
            assert len(newEdge) == 3, 'Only accept (node_i, node_j, weight)!'
            assert isinstance(newEdge[2], int) or isinstance(newEdge[2], float), 'Weight should be integer or float type!'
        else:
            assert len(newEdge) == 2, 'Only accept (node_i, node_j)!'

        if newEdge[0] not in self.node_name_dict or newEdge[1] not in self.node_name_dict:
            print('\n')
            print("Operation failed! 'newEdge' contains unknown node, please check it out or create a new graph instead!")
            print('\n')
        else:
            if not self.weighted:
                self.mat[self.node_name_dict[newEdge[0]]][self.node_name_dict[newEdge[1]]] = 1
                if not self.directed:
                    self.mat[self.node_name_dict[newEdge[1]]][self.node_name_dict[newEdge[0]]] = 1
            else:
                self.mat[self.node_name_dict[newEdge[0]]][self.node_name_dict[newEdge[1]]] = newEdge[2]
                if not self.directed:
                    self.mat[self.node_name_dict[newEdge[1]]][self.node_name_dict[newEdge[0]]] = newEdge[2]

    def delete(self, edge):
        """Delete the specific edge"""
        assert len(edge) in [2, 3], 'Illegal input format!'
        if edge[0] not in self.node_name_dict or edge[1] not in self.node_name_dict:  # 若节点不存在则操作失败
            print('Operation failed! Can not delete edge of unavailable nodes!')
        else:
            self.mat[self.node_name_dict[edge[0]]][self.node_name_dict[edge[1]]] = 0
            if not self.directed:  # 若为无向图，则对称位置置0
                self.mat[self.node_name_dict[edge[1]]][self.node_name_dict[edge[0]]] = 0


if __name__ == '__main__':
    nodes = 4
    edges = [('A', 'C', 1), ('A', 'D', 2), ('B', 'A', 6), ('C', 'B', 3), ('C', 'D', 4), ('D', 'B', 5)]
    new_graph = MatrixGraph(nodes, edges, directed=True, weighted=True)
    print(new_graph)

    new_graph.add_newEdges(('A', 'B', 7))
    print(new_graph)

    new_graph.delete(('A', 'B'))
    print(new_graph)
