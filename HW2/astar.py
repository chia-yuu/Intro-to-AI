import csv
import heapq
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'

def astar(start, end):
    # Begin your code (Part 6)
    # raise NotImplementedError("To be implemented")
    """
    explain part 4 code
    Implement A* search to find the shortes path.
    First initialize the return values and read two csv files.
    When reading edges.csv, we construct the adjlist to represent the graph.
    When reading heuristic.csv, we construct f_vaule to record f for every node, the distance from start passing node to end.
    Remember to change the variable dest1, dest2, dest3 for test1, test2, test3.
    Then start A* search algorithm.
    Use `heapq` to make `openlist` a max heap, where `openlist` store the node and its f.
    In each iteration, we get the node, `cur` with the smallest f in `openlist` and mark it as visit.
    If it is not `start`, subtract h_vaule[int(cur)] from it.
    Go through adjlist to find all neighbors, `nd`, of `cur`.
    If we haven't visited `nd`, check if it is `end`.
    If yes, we have found the path and therefore we can break the while loop.
    If no, check whether f_vaule[nd] > f_new.
    If yes, push `nd` into `openlist` and update `pre_node`.
    After we finish A* search, we can construct the shortest path and compute `dist` by `pre_node`.
    Return path, dist, num_visited.
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

    # What is f_value[nd]? It can be seen as the "total" distance from start, passing nd, to end.
    h_vaule = {}    # h_value[node] = [float h]
    g_value = {}    # g_value[node] = [float g]
    f_value = {}    # f_value[node] = [float f] = g + h
    with open(heuristicFile) as file:
        line_list = [line.rstrip() for line in file]
        for line_idx in range(1, len(line_list)):
            node, dest1, dest2, dest3 = line_list[line_idx].split(",")
            h_vaule[int(node)] = float(dest1)   # change dest i for test i !!!
            g_value[int(node)] = 0.0
            f_value[int(node)] = float('inf')

    # A*
    open_list = []  # (float(f), int(node))
    heapq.heappush(open_list, (0.0, start))
    visit = set()
    pre_node = {}
    reach_end = False
    while len(open_list)>0:
        tmp = heapq.heappop(open_list)  # int
        cur_dist = tmp[0]
        cur = tmp[1]
        visit.add(cur)


        """
        Why cur_dist -= h_vaule[int(cur)] ?
        To compute f_new later, f_new = f[dest] = f[cur] - h[cur] + distance between cur and dest + h[dest]. (Draw a simple graph then it would be clear)
        Notice that cur_dist is actually f[cur].
        But if cur is start, f[start] = 0 and f[cur] - h[cur] will be negative.
        So we use an if statement here to check whether to do f[cur] - h[cur]
        instead of directely write f_new = f[dest] = f[cur] - h[cur] + distance between cur and dest + h[dest] in the later code.
        Then later in the for loop else, f_new become cur_dist + distance +h[dest].
        """
        if cur != start:
            cur_dist -= h_vaule[int(cur)]

        if cur not in adjlist:
            continue
        for nd in adjlist[cur]:
            dest, distance, speed = nd[0], nd[1], nd[2]
            if dest not in visit:
                if dest == end:
                    pre_node[dest] = (cur, distance)
                    reach_end = True
                    visit.add(dest)
                    break   # break for
                else:
                    # g_new = g_value[cur]+float(distance)+cur_dist
                    # h_new = h_vaule[cur]
                    # # f_new = g_new + h_new
                    f_new = cur_dist+distance+h_vaule[dest]
                    if f_value[dest] == float('inf') or f_value[dest]>f_new:
                        heapq.heappush(open_list, (f_new, int(dest)))
                        # g_value[int(dest)] = g_new
                        f_value[int(dest)] = f_new
                        pre_node[int(dest)] = (cur, distance)
        if reach_end:
            break   # break while
                        
    # construct path
    cur = end
    path.append(end)
    while cur!=start:
        cur, distance = pre_node[cur][0], pre_node[cur][1]
        path.insert(0, cur)
        dist += float(distance)

    num_visited = len(visit)

    return path, dist, num_visited
    # End your code (Part 6)


if __name__ == '__main__':
    path, dist, num_visited = astar(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
