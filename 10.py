def find_heads(topo):
    heads = []
    for i, row in enumerate(topo):
        for j, height in enumerate(row):
            if height == 0:
                heads.append((i, j))
    return heads

def explore(topo, x, y, visited):
    rows, cols = len(topo), len(topo[0])
    if (x, y) in visited:
        return set()

    visited.add((x, y))
    reachable_nines = set()

    if topo[x][y] == 9:
        reachable_nines.add((x, y))
        return reachable_nines

    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)] :
        nx, ny = x + dx, y + dy

        if 0 <= nx < rows and 0 <= ny < cols:
            if topo[nx][ny] == topo[x][y] + 1:
                reachable_nines.update(explore(topo, nx, ny, visited))

    return reachable_nines

def score(topo, trailhead):
    visited = set()
    x, y = trailhead
    return len(explore(topo, x, y, visited))

def solve_part1(topo):
    heads = find_heads(topo)
    
    total = 0
    for trailhead in heads:
        total += score(topo, trailhead)

    return total

def count_trails(topo, x, y, memo):
    rows, cols = len(topo), len(topo[0])

    if (x, y) in memo:
        return memo[(x, y)]

    if topo[x][y] == 9:
        return 1

    total_trails = 0

    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy

        if 0 <= nx < rows and 0 <= ny < cols:
            if topo[nx][ny] == topo[x][y] + 1:
                total_trails += count_trails(topo, nx, ny, memo)

    memo[(x, y)] = total_trails
    return total_trails

def rating(topo, trailhead):
    memo = {}
    x, y = trailhead
    return count_trails(topo, x, y, memo)

def solve_part2(topo):
    heads = find_heads(topo)

    total = 0
    for trailhead in heads:
        total += rating(topo, trailhead)

    return total

def read(fn):
    with open(fn, 'r') as file:
        lines = file.read().strip().split('\n')
    return lines

def parse_topo(lines):
    return [list(map(int, line)) for line in lines]

# Test
topo_strings = [
    '89010123',
    '78121874',
    '87430965',
    '96549874',
    '45678903',
    '32019012',
    '01329801',
    '10456732'
]

topo = parse_topo(topo_strings)
print('Part1 :', solve_part1(topo))
print('Part2 :', solve_part2(topo))

# Real
topo_strings = read('data/data10')
topo = parse_topo(topo_strings)
print('Part1 :', solve_part1(topo))
print('Part2 :', solve_part2(topo))
