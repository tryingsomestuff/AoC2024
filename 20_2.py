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
    path = {}

    while queue:
        x, y, steps = queue.popleft()
        
        if (x, y) == end:
            return steps, path
        
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited:
                if maze[nx][ny] != '#':
                    visited.add((nx, ny))
                    path[(nx, ny)] = (x, y)
                    queue.append((nx, ny, steps + 1))
    
    return -1, path

def reconstruct_path(path, start, end):
    current = end
    reconstructed_path = []
    while current != start:
        reconstructed_path.append(current)
        current = path[current]
    reconstructed_path.append(start)
    return reconstructed_path[::-1]

def solve_part2(maze, start, end, path, threshold, max_step):
    cheats = set()
    base_time, path = bfs(maze, start, end)
    best_path = reconstruct_path(path, start, end)

    #print('base_time',base_time)
    #print('path',path)
    #print('best_path',best_path)

    print()
    for i in range(len(best_path)):
        print('\r', i+1, '/', len(best_path), end='')
        for j in range(i + 1, len(best_path)):
            #print('\n', i,j)
            cheat_start = best_path[i]
            cheat_end = best_path[j]
            #print(best_path[i][0], best_path[i][1], best_path[j][0], best_path[j][1])
            #print(abs(best_path[i][0] - best_path[j][0]))
            #print(abs(best_path[i][1] - best_path[j][1]))
            if abs(best_path[i][0] - best_path[j][0]) + abs(best_path[i][1] - best_path[j][1]) <= max_step:
                #print('connects')
                if (j-i) - (abs(best_path[i][0] - best_path[j][0]) + abs(best_path[i][1] - best_path[j][1])) >= threshold:
                    cheats.add((cheat_start, cheat_end))
                    #print('ok')
            #print('########')

    print()    
    return len(cheats)

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
result = solve_part2(maze, start, end, {}, 70, 20)
print('Number of cheats saving :', result)

# Real
maze = read('data/data20')
maze = [list(row) for row in maze]
start, end = parse_maze(maze)
result = solve_part2(maze, start, end, {}, 100, 20)
print('Number of cheats saving :', result)
