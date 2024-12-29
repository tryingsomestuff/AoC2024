from collections import deque

def fence_price(garden_map):
    rows = len(garden_map)
    cols = len(garden_map[0])

    visited = [[False for _ in range(cols)] for _ in range(rows)]

    def bfs(start_row, start_col):
        t = garden_map[start_row][start_col]
        queue = deque([(start_row, start_col)])
        visited[start_row][start_col] = True

        area = 0
        perimeter = 0

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            row, col = queue.popleft()
            area += 1

            for dr, dc in directions:
                nr, nc = row + dr, col + dc

                if 0 <= nr < rows and 0 <= nc < cols:
                    if garden_map[nr][nc] == t and not visited[nr][nc]:
                        visited[nr][nc] = True
                        queue.append((nr, nc))
                    elif garden_map[nr][nc] != t:
                        perimeter += 1
                else:
                    perimeter += 1

        return area, perimeter

    total_price = 0

    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:
                area, perimeter = bfs(r, c)
                total_price += area * perimeter

    return total_price

def read(fn):
    with open(fn, 'r') as file:
        lines = file.read().strip().split('\n')
    return lines

# Test
input = [
    'RRRRIICCFF',
    'RRRRIICCCF',
    'VVRRRCCFFF',
    'VVRCCCJFFF',
    'VVVVCJJCFE',
    'VVIVCCJJEE',
    'VVIIICJJEE',
    'MIIIIIJJEE',
    'MIIISIJEEE',
    'MMMISSJEEE'
]

garden_map = [list(row) for row in input]
price = fence_price(garden_map)
print('Total price:', price)

# Real
input = read('data/data12')

garden_map = [list(row) for row in input]
price = fence_price(garden_map)
print('Total price:', price)
