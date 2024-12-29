import heapq

# Part 2

def dijkstra(maze):
    directions = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}
    opp_directions = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
    
    start, end = None, None
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == 'S':
                start = (i, j)
            elif cell == 'E':
                end = (i, j)
    
    if not start or not end:
        return -1, []

    pq = []
    for d in directions:
        initial_cost = 1000 if d != 'E' else 0  # Add 1000 if starting direction is not East
        heapq.heappush(pq, (initial_cost, start, d, [start]))  # (cost, position, direction, path)

    visited = {}
    best_paths = []
    min_cost = float('inf')

    while pq:
        cost, (x, y), current_dir, path = heapq.heappop(pq)

        if (x, y) == end:
            # this time we will record all best paths
            if cost < min_cost:
                min_cost = cost
                best_paths = [path]
            elif cost == min_cost:
                best_paths.append(path)
            continue

        if ((x, y), current_dir) in visited and visited[((x, y), current_dir)] < cost:
            continue

        visited[((x, y), current_dir)] = cost

        for new_dir, (dx, dy) in directions.items():
            if new_dir == opp_directions[current_dir]:
                continue            
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] != '#':
                move_cost = 1 if current_dir == new_dir else 1001
                new_cost = cost + move_cost
                heapq.heappush(pq, (new_cost, (nx, ny), new_dir, path + [(nx, ny)]))

    return min_cost, best_paths

def display(maze, path):
    maze_copy = [row[:] for row in maze]

    for i, j in path:
        if maze_copy[i][j] not in ('S', 'E'):
            maze_copy[i][j] = 'o'

    return '\n'.join(''.join(row) for row in maze_copy)

def solve_part2(maze):
    maze = [list(row) for row in maze]
    result_cost, result_paths = dijkstra(maze)
    print('Shortest path cost:', result_cost)

    # Remove duplicates ...
    #print('All best paths:')
    all = set()
    for path in result_paths:
        #print(path)
        #print(display(maze,path))
        for p in path:
            all.add(p)

    #print(display(maze,all))
    print(len(all))    

def read(fn):
    with open(fn, 'r') as file:
        lines = file.read().strip().split('\n')
    return lines

# Test 1
maze = [
    '###############',
    '#.......#....E#',
    '#.#.###.#.###.#',
    '#.....#.#...#.#',
    '#.###.#####.#.#',
    '#.#.#.......#.#',
    '#.#.#####.###.#',
    '#...........#.#',
    '###.#.#####.#.#',
    '#...#.....#.#.#',
    '#.#.#.###.#.#.#',
    '#.....#...#.#.#',
    '#.###.#.#.#.#.#',
    '#S..#.....#...#',
    '###############',
]

solve_part2(maze)


# Test 2
maze = [
    '#################',
    '#...#...#...#..E#',
    '#.#.#.#.#.#.#.#.#',
    '#.#.#.#...#...#.#',
    '#.#.#.#.###.#.#.#',
    '#...#.#.#.....#.#',
    '#.#.#.#.#.#####.#',
    '#.#...#.#.#.....#',
    '#.#.#####.#.###.#',
    '#.#.#.......#...#',
    '#.#.###.#####.###',
    '#.#.#...#.....#.#',
    '#.#.#.#####.###.#',
    '#.#.#.........#.#',
    '#.#.#.#########.#',
    '#S#.............#',
    '#################'
]

solve_part2(maze)


# Real
maze = maze = read('data/data16')

solve_part2(maze)
