from collections import deque

def shortest_path(falling_bytes, grid_size, max_steps):
    grid = [['.' for _1 in range(grid_size)] for _2 in range(grid_size)]

    for step, (x, y) in enumerate(falling_bytes):
        if step >= max_steps:
            break
        grid[y][x] = '#'

    def bfs():
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        queue = deque([(0, 0, 0, [])])
        visited = set()
        visited.add((0, 0))

        while queue:
            x, y, steps, path = queue.popleft()

            if (x, y) == (grid_size - 1, grid_size - 1):
                return steps, path + [(x, y)]

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < grid_size and 0 <= ny < grid_size:
                    if (nx, ny) not in visited and grid[ny][nx] == '.':
                        visited.add((nx, ny))
                        queue.append((nx, ny, steps + 1, path + [(x, y)]))

        return -1, []

    return bfs(), grid

def read(fn):
    falling_bytes = []
    with open(fn, 'r') as file:
        for line in file:
            x, y = map(int, line.strip().split(','))
            falling_bytes.append((x, y))
    return falling_bytes

# Part 1

# Test
grid_size = 7
max_steps = 12
falling_bytes = read('data/data18_sample')

(result, path), grid = shortest_path(falling_bytes, grid_size, max_steps)
print('Shortest path length:', result)

# Real 
grid_size = 71
max_steps = 1024
falling_bytes = read('data/data18')

(result, path), grid = shortest_path(falling_bytes, grid_size, max_steps)
print('Shortest path length:', result)

# Part 2

def draw_grid(grid, path=None):
    path_set = set(path) if path else set()
    for y, row in enumerate(grid):
        line = ''
        for x, cell in enumerate(row):
            if (x, y) in path_set:
                line += 'O'
            else:
                line += cell
        print(line)

#print('Grid:')
#draw_grid(grid, path)

while(True):
    max_steps +=1
    (result, path), grid = shortest_path(falling_bytes, grid_size, max_steps)
    if result == -1:
        print('Shortest path length:', result, max_steps, falling_bytes[max_steps-1])
        break