import math

def parse_map(input_map):
    antennas = []
    for y, line in enumerate(input_map):
        for x, char in enumerate(line):
            if char != '.':
                antennas.append((char, x, y))
    return antennas

def get_all_line_points(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    
    gcd = math.gcd(dx, dy)
    
    step_x = dx // gcd
    step_y = dy // gcd
    
    points = []

    # kinda brut-force ...    
    temp_x, temp_y = x1, y1
    for i in range(50): 
        points.append((temp_x, temp_y))
        temp_x -= step_x
        temp_y -= step_y
    
    temp_x, temp_y = x1, y1
    for i in range(50):
        if i != 0:
            points.append((temp_x, temp_y))
        temp_x += step_x
        temp_y += step_y
    
    return points

def calculate_antinodes(antennas, width, height):
    antinodes = set()

    freq_map = {}
    for freq, x, y in antennas:
        if freq not in freq_map:
            freq_map[freq] = []
        freq_map[freq].append((x, y))

    for freq, locations in freq_map.items():
        n = len(locations)
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                x1, y1 = locations[i]
                x2, y2 = locations[j]

                line_points = get_all_line_points(x1, y1, x2, y2)
                
                for point in line_points:
                    if 0 <= point[0] < width and 0 <= point[1] < height: 
                        antinodes.add(point)

    return antinodes

def build_map_with_antinodes(input_map, antinodes):
    map_with_antinodes = [list(row) for row in input_map]

    for x, y in antinodes:
        if map_with_antinodes[y][x] == '.':
            map_with_antinodes[y][x] = '#'
        else:
            pass#map_with_antinodes[y][x] = '$'

    return [''.join(row) for row in map_with_antinodes]
    
def count_antinodes(input_map):
    antennas = parse_map(input_map)
    height = len(input_map)
    width = len(input_map[0]) if height > 0 else 0

    antinodes = calculate_antinodes(antennas, width, height)

    #print(antinodes)

    return len(antinodes), antinodes

def solve_part2(input_map):
    count, antinodes = count_antinodes(input_map)

    map_with_antinodes = build_map_with_antinodes(input_map, antinodes)
    #print('\n'.join(map_with_antinodes))

    print(count)

def read(fn):
    with open(fn, 'r') as file:
        lines = file.read().strip().split('\n')
    return lines

# Test
input_map = [
'............',
'........0...',
'.....0......',
'.......0....',
'....0.......',
'......A.....',
'............',
'............',
'........A...',
'.........A..',
'............',
'............'
]

solve_part2(input_map)

# Real
input_map = read('data/data08')

solve_part2(input_map)
