import csv
edgeFile = 'edges.csv'


def dfs(start, end):
    # Begin your code (Part 2)
    # raise NotImplementedError("To be implemented")
    """
    explain part 2 code (stack)
    Use stack to implement a iteretive DFS.
    This is similar to what we did in part 1, just change the queue to stack.
    First initialize the return values and read file as what we did in part 1.
    Then start DFS with stack `st`.
    In each iteration, check whether the current node, `cur`, is accessable.
    That is, whether `cur` has been recorded in `pre_node`. If yes, we have found the path, ad we can break.
    Otherwise, check whether we had visited `cur`. (if cur in visit)
    If yes, skip this node and continue. Otherwise, mark `cur` as visited.
    Iterate through all the node in `adjlist`, push the neighbors of `cur` into the stack `st`.
    After we finish DFS, we can construct `path` and compute `dist` by `pre_node` like what we did in part 1.
    We start from `end` and back track. Using `pre_node` to find the previous node of each node.
    Return path, dist, num_visited back.
    """

    # init
    path = []       # list of int
    dist = 0.0      # float
    num_visited = 0 # int

    # read file
    adjlist = {}
    with open(edgeFile) as file:
        line_list = [line.rstrip() for line in file]
        for line_idx in range(1, len(line_list)):
            src, dest, distance, speed = line_list[line_idx].split(",")
            if int(src) not in adjlist:
                adjlist[int(src)] = []
            adjlist[int(src)].append((int(dest), float(distance), float(speed)))        
    
    # dfs with stack
    st = []     # stack<int>
    visit = set()
    pre_node = {}   # dict<int, (int, str, str)> to record the previous node
    st.append(start)
    while len(st)>0:
        cur = st.pop()
        if end in pre_node:
            visit.add(end)
            num_visited+=1
            break
        if cur in visit:
            continue
        else:
            visit.add(cur)
            num_visited+=1

        # go through adjlist to push cur's neighbor to st
        if cur not in adjlist:
            continue

        for nd in adjlist[cur]:
            dest, distance, speed = nd[0], nd[1], nd[2]
            if int(dest) not in visit:
                st.append(int(dest))
                pre_node[int(dest)] = (cur, distance, speed)
                

    # trace back to construct path
    path.append(end)
    cur = end
    while cur != start:
        cur, distance = pre_node[cur][0], pre_node[cur][1]
        path.insert(0, cur)
        dist += float(distance)

    return path, dist, num_visited
    # End your code (Part 2)


if __name__ == '__main__':
    path, dist, num_visited = dfs(1718165260, 8513026827)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')


"""
1st
The number of path nodes: 222
Total distance of path: 11061.247
The number of visited nodes: 12054

2nd
The number of path nodes: 214
Total distance of path: 10739.767000000002
The number of visited nodes: 12053

bfs
The number of path nodes: 88
Total distance of path: 4978.881999999998
The number of visited nodes: 4131

The number of path nodes: 1232
Total distance of path: 57208.987
The number of visited nodes: 4211
"""