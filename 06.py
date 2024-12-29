
DIRECTIONS = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1)
}

DIRECTION_ORDER = list(DIRECTIONS.keys()) # must be in the good order, so Python >=3.7 requiered !!!
#print(DIRECTION_ORDER)

def init(grid_input):
    rows, cols = len(grid_input), len(grid_input[0])
    obstacles = set()
    guard_position = None
    guard_direction = None

    for r in range(rows):
        for c in range(cols):
            char = grid_input[r][c]
            if char == '#':
                obstacles.add((r, c))
            elif char in DIRECTION_ORDER:
                guard_position = (r, c)
                guard_direction = char

    return rows, cols, obstacles, guard_position, guard_direction

def move_guard(position, direction):
    r, c = position
    dr, dc = DIRECTIONS[direction]
    return r + dr, c + dc

def simulate_guard_path(rows, cols, obstacles, guard_position, guard_direction):

    visited_positions = set()
    visited_positions.add((guard_position,guard_direction))
    
    while True:
        nr, nc = move_guard(guard_position, guard_direction)
        #print(nr,nc)

        # exit
        if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
            return visited_positions, False

        # loop
        if ((nr,nc),guard_direction) in visited_positions:
            return visited_positions, True

        if (nr,nc) in obstacles:
            # rotate
            current_index = DIRECTION_ORDER.index(guard_direction)
            guard_direction = DIRECTION_ORDER[(current_index + 1) % 4]
        else:
            # update
            guard_position = (nr,nc)
            visited_positions.add((guard_position,guard_direction))

def solve_part1(grid_input):

    rows, cols, obstacles, guard_position, guard_direction = init(grid_input)
    path, loop = simulate_guard_path(rows, cols, obstacles, guard_position, guard_direction)

    filtered = { p for p, d in path}
    if loop:
        print('loop:', len(filtered))
    else:
        print('exit:', len(filtered))

def solve_part2(grid_input):

    rows, cols, obstacles, guard_position, guard_direction = init(grid_input)
    path, loop = simulate_guard_path(rows, cols, obstacles, guard_position, guard_direction)

    # brute force ...
    def count_loop_positions(grid, path):
        possible_positions = 0
        for r in range(len(grid)):
            print(r+1, '/', len(grid))
            for c in range(len(grid[0])):
                if grid[r][c] == '.':
                    new_obstacles = {o for o in obstacles}
                    new_obstacles.add((r,c))
                    path, loop = simulate_guard_path(rows, cols, new_obstacles, guard_position, guard_direction)

                    if loop:
                        #print(r, c, loop, path)
                        possible_positions += 1
        return possible_positions

    path = simulate_guard_path(rows, cols, obstacles, guard_position, guard_direction)
    loop_positions = count_loop_positions(grid_input, path)

    print(f'Number of loops: {loop_positions}')

def read(fn):
    with open(fn, 'r') as file:
        lines = file.read().strip().split('\n')
    return lines

# Test
grid_input = [
'....#.....',
'.........#',
'..........',
'..#.......',
'.......#..',
'..........',
'.#..^.....',
'........#.',
'#.........',
'......#...'
]

solve_part1(grid_input)
solve_part2(grid_input)

# Real
grid_input = read('data/data06')

solve_part1(grid_input)
solve_part2(grid_input)
