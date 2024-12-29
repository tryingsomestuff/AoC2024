from collections import Counter

def solve_part1(grid):
    word = 'XMAS'
    word_len = len(word)
    rows = len(grid)
    cols = len(grid[0])

    directions = [
        (0, 1),   
        (0, -1),  
        (1, 0),   
        (-1, 0),  
        (1, 1),   
        (-1, -1), 
        (1, -1),  
        (-1, 1)   
    ]

    def check_word(r, c, dr, dc):
        for i in range(word_len):
            nr, nc = r + i * dr, c + i * dc
            # out of bound or bad letter
            if not (0 <= nr < rows and 0 <= nc < cols) or grid[nr][nc] != word[i]:
                return False
        return True

    count = 0

    # let's try everything ...
    for r in range(rows):
        for c in range(cols):
            for dr, dc in directions:
                if check_word(r, c, dr, dc):
                    count += 1

    print(count)

def solve_part2(grid):
    rows = len(grid)
    cols = len(grid[0])

    directions = [
        (1, 1), 
        (1, -1),
        (-1, 1),
        (-1, -1)
    ]
    
    def is_xmas(r, c, dr, dc):
        if (0 <= r < rows and 0 <= c < cols and
            0 <= r + dr < rows and 0 <= c + dc < cols and
            0 <= r - dr < rows and 0 <= c - dc < cols):
            return (grid[r][c] == 'A' and  
                    grid[r + dr][c + dc] == 'M' and  
                    grid[r - dr][c - dc] == 'S' 
            )
        return False

    count = 0
    coords = []
    # try everything ...
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            for dr, dc in directions:
                if is_xmas(r, c, dr, dc):
                    #print(r,c)
                    coords.append([r,c])
    
    def count_only_twice(l):
        count = Counter(tuple(coord) for coord in l)
        return sum(1 for v in count.values() if v == 2)

    print(count_only_twice(coords))

def read(fn):
    with open(fn, 'r') as file:
        lines = file.read().strip().split('\n')
    return lines

grid = [
    'MMMSXXMASM',
    'MSAMXMSMSA',
    'AMXSXMAAMM',
    'MSAMASMSMX',
    'XMASAMXAMM',
    'XXAMMXXAMA',
    'SMSMSASXSS',
    'SAXAMASAAA',
    'MAMMMXMMMM',
    'MXMXAXMASX'
]

solve_part1(grid)
solve_part2(grid)

grid = read('data/data04')

solve_part1(grid)
solve_part2(grid)
