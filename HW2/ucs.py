import csv
import heapq
edgeFile = 'edges.csv'


def ucs(start, end):
    # Begin your code (Part 3)
    # raise NotImplementedError("To be implemented")
    """
    explain part 3 code
    Implement a uniform cost search function to find the shortest path.
    First, initialize the return value and read the csv file as adjlist.
    Then start UCS with heap `pq`.
    `pq` has distance, current node, and previous node,
    where distance is the distance from start to current node.
    In each iteration, we get the node with the shortest distance.
    If we haven't visited the node yet, we mark it as visit and update `pre_node`.
    If the current is already the end node, we can break the whiel loop.
    Otherwise, go through all the neighbors of current node and push them into `pq`.
    After we finish UCS, we can construct the path by back tracking.
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

             
    # Uniform-Cost Search
    pq = []
    heapq.heappush(pq, (0.0, start, -1))    # (dist, cur, pre)
    pre_node = {}
    visit = set()
    while len(pq)>0:
        distance, cur, pre = heapq.heappop(pq)

        if cur not in visit:
            visit.add(cur)
            pre_node[int(cur)] = int(pre)

            if cur == end:
                dist = distance
                num_visited = len(visit)
                break
            
            if cur not in adjlist:
                continue

            for nd in adjlist[cur]:
                dest, tmp_d, speed = nd[0], nd[1], nd[2]
                heapq.heappush(pq, (distance+tmp_d, dest, cur))
        
    # trace back to construct path
    path.append(end)
    cur = end
    while cur != start:
        cur = pre_node[cur]
        path.insert(0, cur)

    return path, dist, num_visited
    # End your code (Part 3)


if __name__ == '__main__':
    path, dist, num_visited = ucs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
