import csv
import queue
edgeFile = 'edges.csv'


def bfs(start, end):
    # Begin your code (Part 1)
    # raise NotImplementedError("To be implemented")
    """
    explain part 1 code
    Use BFS to find the path.
    First, initialize the return value and read the csv file as adjlist.
    Then we can start BFS.
    Use queue `q` to record the node to visit, set `visit` to record the node that we had visited.
    If we can access `end`, then we have found the path, so break the while loop.
    If we had visited the node, `cur`, then skip it and continue.
    Otherwise, add the curent node to `visit`.
    Then we go through `adjlist` to find all the neighbors of curent node,
    push them into the queue `q` and record their previous node for later use.
    (`pre_node` is a dict to store each node's ancestor and the distance to its ancestor)
    After we finish BFS, we had found the path, then we can construct it by back tracking.
    From `end`, use `pre_node` to find the previous node of each node to construct the path and compute `dist`.
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
            # adjlist.append((str(src), str(dest), str(distance), str(speed)))
            if int(src) not in adjlist:
                adjlist[int(src)] = []
            adjlist[int(src)].append((int(dest), float(distance), float(speed)))
        
    # print("adjlist:")
    # print(adjlist[1079387396])
    # print(adjlist[8540463858])
    
    # bfs
    q = queue.Queue()
    visit = set()
    pre_node = {}   # dict<int, (int, str, str)> to record the previous node
    q.put(start)
    while not q.empty():
        cur = q.get()
        if end in pre_node:
            num_visited+=1
            break
        if cur in visit:
            continue

        visit.add(cur)
        num_visited+=1
       
        if cur not in adjlist:
            continue
        
        for nd in adjlist[cur]:
            dest, distance, speed = nd[0], nd[1], nd[2]
            if int(dest) not in pre_node:
                q.put(int(dest))
                pre_node[int(dest)] = (cur, distance, speed)

    # print("pre_node:")
    # print(pre_node[1079387396])
    # print(pre_node[8540463858])
    # print(pre_node[4413408590])


    # trace back to construct path
    path.append(end)
    cur = end
    while cur != start:
        # print(cur, end = ", ")
        cur, distance = pre_node[cur][0], pre_node[cur][1]
        path.insert(0, cur)
        dist += float(distance)

    return path, dist, num_visited
    # End your code (Part 1)



if __name__ == '__main__':
    path, dist, num_visited = bfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')

"""
path = 
[2270143902, 311080383, 3226037492, 3226037861, 1523225502, 3226037862, 1513884389, 311080382, 2271410308, 5160642090, 2271410307, 311080380, 2272116576, 321706316, 2272116577, 5160642088, 2270157519, 2270157522, 4397305472, 426526844, 2272116586, 426526843, 314947120, 2272116587, 2272116588, 311080375, 311080367, 1726059992, 2617655246, 7462484381, 7462484370, 2348039016, 5160641357, 2348039022, 5621202121, 5160641356, 26069872, 2348039031, 5322031944, 2271561529, 2900201982, 4153548984, 3951197837, 2761345328, 26059491, 313164126, 3012358522, 1756262937, 26069885, 5322031945, 3224991168, 1723026427, 1723037689, 2606055790, 2009106704, 2386842510, 1151731672, 26069924, 1307159377, 1099409403, 1151731322, 2600512303, 3485300283, 6333865581, 321706399, 6333865579, 2600512323, 321706398, 3218814937, 3218814938, 2726738884, 2726738885, 321706397, 368297601, 2078312046, 2385315974, 368297602, 2385315973, 2421243550, 331638852, 1103039716, 1103039576, 1103039646, 321706380, 4401808638, 2042814530, 2421243548, 1079387396]
"""

"""
distance = 
197.982,  39.07,  36.061,  30.877,  90.71,  77.343,  63.405,  21.462,  57.749,  36.462,  82.75,  123.912,  62.5,  60.271,  171.533,  95.063,  124.61,  81.358,  158.592,  24.453,  22.82,  65.355,  7.794,  15.598,  1.705,  44.991,  151.855,  107.064,  61.993,  119.805,  89.784,  40.935,  68.063,  79.687,  142.269,  49.475,  118.878,  24.096,  84.293,  47.92,  22.912,  196.604,  172.443,  13.669,  90.964,  10.152,  103.468,  119.034,  93.422,  32.293,  96.575,  20.971,  33.42,  51.138,  19.997,  34.274,  158.496,  54.946,  14.33,  10.036,  21.226,  13.978,  9.542,  10.071,  8.002,  26.274,  12.285,  11.696,  14.887,  23.78,  70.637,  36.738,  23.826,  17.259,  20.99,  21.258,  37.477,  9.698,  30.547,  78.959,  38.13,  18.088,  22.835,  22.7,  14.642,  22.359,  11.311,  The number of path nodes: 88

speed = 
46.4,  46.4,  46.4,  46.4,  46.4,  46.4,  46.4,  46.4,  46.4,  46.4,  49.3,  49.3,  49.3,  49.3,  49.3,  49.3,  49.3,  49.3,  49.3,  49.3,  49.3,  49.3,  49.3,  49.3,  49.3,  49.3,  49.3,  49.3,  49.3,  50.0,  50.0,  50.0,  50.0,  50.0,  50.0,  50.0,  50.0,  50.0,  50.0,  50.0,  50.0,  50.0,  50.0,  50.0,  50.0,  50.0,  50.0,  50.0,  50.0,  50.0,  50.0,  50.0,  50.0,  50.0,  50.0,  50.0,  50.0,  50.0,  50.0,  50.0,  46.4,  46.4,  46.4,  46.4,  46.4,  46.4,  46.4,  46.4,  46.4,  46.4,  46.4,  46.4,  46.4,  46.4,  46.4,  46.4,  46.4,  46.4,  46.4,  46.4,  46.4,  46.4,  46.4,  46.4,  46.4,  46.4,  46.4,  The number of path nodes: 88
"""