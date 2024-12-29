from collections import deque

def parse_maze(maze):
    start, end = None, None
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == 'S':
                start = (i, j)
            elif cell == 'E':
                end = (i, j)
    return start, end

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def bfs(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    queue = deque([(start[0], start[1], 0)])  # (row, col, steps)
    visited = set()
    visited.add(start)

    while queue:
        x, y, steps = queue.popleft()
        
        if (x, y) == end:
            return steps
        
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited:
                if maze[nx][ny] != '#':
                    visited.add((nx, ny))
                    queue.append((nx, ny, steps + 1))
    
    return -1

def find_removable_walls(maze):
    rows, cols = len(maze), len(maze[0])
    removable_walls = []
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if maze[i][j] == '#':
                # Check if wall connects
                neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                dot_count = sum(1 for x, y in neighbors if maze[x][y] == '.' or maze[x][y] == 'S' or maze[x][y] == 'E')
                if dot_count >= 2:
                    removable_walls.append((i, j))
    return removable_walls

def display_maze(maze):
    for row in maze:
        print(''.join(row))
    print()  

# A dummy, slow, but working way of trying short-cuts
def compute_cheat_lengths(maze, start, end, removable_walls, threshold):
    original_length = bfs(maze, start, end)
    lengths = []
    count = 0

    i = 0
    for wx, wy in removable_walls:
        maze[wx][wy] = '.'
        if i % 1000 == 0:
            print(i,'/',len(removable_walls))
        #print(wx,wy)
        #display_maze(maze)
        new_length = bfs(maze, start, end)
        lengths.append(new_length)
        gain = original_length - new_length
        if gain >= threshold:
            count += 1
        maze[wx][wy] = '#'
        i += 1
    
    return original_length, lengths, count

def solve_part1(maze, start, end, threshold):
    removable_walls = find_removable_walls(maze)
    #print(removable_walls)
    original_length, lengths, count = compute_cheat_lengths(maze, start, end, removable_walls, threshold)

    print(f'Original maze length: {original_length}')
    print('All possible lengths with one wall removed:')
    lengths = sorted(lengths)
    print(lengths[:5])
    print(f'Best gain: {original_length-lengths[0]}')
    print(f'Big gain: {count}')

def read(fn):
    with open(fn, 'r') as file:
        lines = file.read().strip().split('\n')
    return lines

# Test
input_maze = '''
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
'''
maze = [list(row) for row in input_maze.strip().split('\n')]
start, end = parse_maze(maze)
solve_part1(maze, start, end, 40)

# Real
maze = read('data/data20')
maze = [list(row) for row in maze]
start, end = parse_maze(maze)
solve_part1(maze, start, end, 100)
