import heapq

# Part 1

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
        return -1

    pq = []
    for d in directions:
        initial_cost = 1000 if d != 'E' else 0  # Add 1000 if starting direction is not East
        heapq.heappush(pq, (initial_cost, start, d))  # (cost, position, direction)

    visited = {}

    while pq:
        cost, (x, y), current_dir = heapq.heappop(pq)

        if (x, y) == end:
            return cost

        if ((x, y), current_dir) in visited and visited[((x, y), current_dir)] <= cost:
            continue

        visited[((x, y), current_dir)] = cost

        for new_dir, (dx, dy) in directions.items():
            if new_dir == opp_directions[current_dir]:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] != '#':
                move_cost = 1 if current_dir == new_dir else 1001
                new_cost = cost + move_cost
                heapq.heappush(pq, (new_cost, (nx, ny), new_dir))

    return -1

def solve_part1(maze):
    maze = [list(row) for row in maze]
    result = dijkstra(maze)
    print('Shortest path cost:', result)    

def read(fn):
    with open(fn, 'r') as file:
        lines = file.read().strip().split('\n')
    return lines

# Test
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

solve_part1(maze)


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

solve_part1(maze)


# Real
maze = read('data/data16')

solve_part1(maze)
