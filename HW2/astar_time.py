import csv
import heapq
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'


def astar_time(start, end):
    # Begin your code (Part 6)
    # raise NotImplementedError("To be implemented")
    """
    explain part 6 code
    modify A_star.py, the heuristic value is the time instead of the distance (we use distance in A_star.py).
    So the heuristic value = distance / speed. Remember the speed is in km/h, but the distance is in meter,
    so we have to do the conversion.
    Other code are the same as A_star.py. By modifying the heuristic value, we can get the fastest path.
    """

    # init
    path = []       # list of int
    dist = 0.0      # float
    num_visited = 0 # int
    # average speed in edge.csv = 52 km/h = 14 m/s
    avg_speed = 14.0

    # read file
    adjlist = {}
    with open(edgeFile) as file:
        line_list = [line.rstrip() for line in file]
        for line_idx in range(1, len(line_list)):
            src, dest, tmp_time, speed = line_list[line_idx].split(",")
            float_speed = float(speed)*10/36
            if int(src) not in adjlist:
                adjlist[int(src)] = []
            adjlist[int(src)].append((int(dest), float(tmp_time)/float_speed, float(speed)))

    # print(adjlist[2270143902])

    # What is f_value[nd]? It can be seen as the "total" tmp_time from start, passing nd, to end.
    h_vaule = {}    # h_value[node] = [float h]
    f_value = {}    # f_value[node] = [float f]
    with open(heuristicFile) as file:
        line_list = [line.rstrip() for line in file]
        for line_idx in range(1, len(line_list)):
            node, dest1, dest2, dest3 = line_list[line_idx].split(",")
            if float(dest1)==0.0:                               # change dest i for test i !!!
                h_vaule[int(node)] = 0.0
            else:
                h_vaule[int(node)] = float(dest1)/avg_speed     # change dest i for test i !!!
            f_value[int(node)] = float('inf')

    # print(h_vaule[2270143902])

    # A*
    open_list = []  # (float(f), int(node))
    heapq.heappush(open_list, (0.0, start))
    visit = set()
    pre_node = {}
    reach_end = False
    cnt=0
    while len(open_list)>0:
        tmp = heapq.heappop(open_list)  # int
        cur_time = tmp[0]
        cur = tmp[1]
        visit.add(cur)

        if cur != start:
            cur_time -= h_vaule[int(cur)]

        if cur not in adjlist:
            continue
        for nd in adjlist[cur]:
            dest, tmp_time = nd[0], nd[1]
            # if cnt<10:
            #     print(tmp_time, end = ', ')
            #     cnt+=1
            if dest not in visit:
                if dest == end:
                    pre_node[dest] = (cur, tmp_time)
                    reach_end = True
                    visit.add(dest)
                    break   # break for
                else:
                    f_new = cur_time + tmp_time + h_vaule[dest]
                    if f_value[dest] == float('inf') or f_value[dest]>f_new:
                        heapq.heappush(open_list, (f_new, int(dest)))
                        f_value[int(dest)] = f_new
                        pre_node[int(dest)] = (cur, tmp_time)
                        
        if reach_end:
            break   # break while
    
    # construct path
    cur = end
    path.append(end)
    while cur!=start:
        cur, tmp_time = pre_node[cur][0], pre_node[cur][1]
        path.insert(0, cur)
        dist += float(tmp_time)

    num_visited = len(visit)

    return path, dist, num_visited
    # End your code (Part 6)


if __name__ == '__main__':
    path, time, num_visited = astar_time(1718165260, 8513026827)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total second of path: {time} s')
    print(f'The number of visited nodes: {num_visited}')
