import csv
import sys
edgeFile = 'edges.csv'


def dfs(start, end):
    # Begin your code (Part 2)
    # raise NotImplementedError("To be implemented")
    """
    explain part 2 code (recursive)
    Implement DFS by recursion.
    First initialize the return values and read the file as adjlist.
    Then define another function `dfs_recur` to perform recursion.
    Notice that before we call `dfs_recur`, there is `sys.setrecursionlimit(10000000)`.
    It is to set the maximum depth of the Python interpreter stack to 10000000.
    Otherwise, it will give the error message, "maximum recursion depth exceeded while calling a Python object".
    In `dfs_recur`, `node` represent the current node we are visiting.
    Mark `node` as visit and go through all its neighbor,
    Run `dfs_recur` for every neighbor.
    If we can reach `end` (end in pre_node), then we found the path and we can return.
    After finish `dfs_recur`, we can construct the path, compute dist, and return path, dist, num_visited
    """

    # init
    path = []       # list of int
    dist = 0.0      # float
    num_visited = 0 # int

    # read file
    adjlist = []
    # adjlist = [('26059311', '3256115046', '53.141', '50.0'), ('26059311', '4429332928', '11.548', '46.4'), ('26059311', '4419128653', '14.588', '50.0'), ...]
    with open(edgeFile) as file:
        line_list = [line.rstrip() for line in file]
        for line_idx in range(1, len(line_list)):
            src, dest, distance, speed = line_list[line_idx].split(",")
            adjlist.append((str(src), str(dest), str(distance), str(speed)))


    # recursive dfs, int node
    visit = set()
    pre_node = {}   # dict<int, (int, str, str)> to record the previous node
    
    # call recursive dfs
    sys.setrecursionlimit(10000000)
    dfs_recur(start, end, pre_node, visit, adjlist)

    # construct path
    cur = end
    path.append(cur)
    while cur != start:
        cur, d = pre_node[cur][0], pre_node[cur][1]
        path.insert(0, int(cur))
        dist += float(d)
        
    num_visited = len(visit)

    return path, dist, num_visited
    # End your code (Part 2)

def dfs_recur(node : int, end : int, pre_node : dict, visit : set, adjlist : list):
    visit.add(node)
    for nd in adjlist:
        src, dest, distance, speed = nd[0], nd[1], nd[2], nd[3]
        if int(src) == node and not (int(dest) in visit):
            pre_node[int(dest)] = (int(src), distance, speed)
            dfs_recur(int(dest), end, pre_node, visit, adjlist)
            if end in pre_node:
                break


if __name__ == '__main__':
    path, dist, num_visited = dfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
