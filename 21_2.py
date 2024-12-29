from collections import deque
from collections import Counter

debug = False

memo_bfs = {}
memo_pad = {}

def create_keypad_graph(keypad):
    rows = len(keypad)
    cols = len(keypad[0])
    graph = {}

    for r in range(rows):
        for c in range(cols):
            if keypad[r][c] == ' ':
                continue
            neighbors = []
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and keypad[nr][nc] != ' ':
                    neighbors.append((nr, nc))
            graph[(r, c)] = neighbors

    return graph

def bfs_all_shortest_paths(graph, start, goal, use_cache):
    global memo_bfs

    queue = deque([(start, [start])])
    visited = set()
    shortest_paths = []
    shortest_length = None

    if use_cache and (start, goal) in memo_bfs:
        return memo_bfs[(start, goal)]

    while queue:
        current, path = queue.popleft()

        if current in visited and (shortest_length is not None and len(path) > shortest_length):
            continue

        if current == goal:
            if shortest_length is None:
                shortest_length = len(path)
            if len(path) == shortest_length:
                shortest_paths.append(path)
            continue

        visited.add(current)

        for neighbor in graph[current]:
            if neighbor not in path:
                queue.append((neighbor, path + [neighbor]))

    if use_cache:
        memo_bfs[(start, goal)] = shortest_paths

    return shortest_paths

def compute_sequence(keypad_graph, start_pos, code, keypad_map, use_cache):
    if debug: print('---compute_sequence', start_pos, code)
    #if debug: print('---compute_sequence', keypad_graph)
    current_pos = start_pos
    all_sequences = [[]]

    for char in code:
        target_pos = keypad_map[char]
        if debug: print('---compute_sequence', char, target_pos, current_pos)
        all_paths = bfs_all_shortest_paths(keypad_graph, current_pos, target_pos, use_cache)
        all_path_commands = [path_to_commands(path) for path in all_paths]
        if debug: print('---all_paths', all_paths)
        if debug: print('---all_path_commands', all_path_commands)
        all_sequences = [
            existing_sequence + new_commands
            for existing_sequence in all_sequences
            for new_commands in all_path_commands
        ]
        current_pos = target_pos

    return all_sequences, current_pos 

def path_to_commands(path):
    commands = []
    for (r1, c1), (r2, c2) in zip(path, path[1:]):
        if r2 < r1:
            commands.append('^')
        elif r2 > r1:
            commands.append('v')
        elif c2 < c1:
            commands.append('<')
        elif c2 > c1:
            commands.append('>')
    commands.append('A')
    return commands

def transform(sequence):
    result = []
    prev_char = 'A'
    for char in sequence:
        if prev_char == 'A':
            if char == '^':
                result.append('<A')
            elif char == '>':
                result.append('vA')
            elif char == 'v':
                result.append('<vA')
            elif char == '<':
                result.append('v<<A')
            elif char == 'A':
                result.append('A')

        elif prev_char == '>':
            if char == '^':
                result.append('<^A')
            elif char == '>':
                result.append('A')
            elif char == 'v':
                result.append('<A')
            elif char == '<':
                result.append('<<A')
            elif char == 'A':
                result.append('^A')

        elif prev_char == '^':
            if char == '^':
                result.append('A')
            elif char == '>':
                result.append('v>A')
            elif char == 'v':
                result.append('vA')
            elif char == '<':
                result.append('v<A')
            elif char == 'A':
                result.append('>A')

        elif prev_char == 'v':
            if char == '^':
                result.append('^A')
            elif char == '>':
                result.append('>A')
            elif char == 'v':
                result.append('A')
            elif char == '<':
                result.append('<A')
            elif char == 'A':
                result.append('^>A')

        elif prev_char == '<':
            if char == '^':
                result.append('>^A')
            elif char == '>':
                result.append('>>A')
            elif char == 'v':
                result.append('>A')
            elif char == '<':
                result.append('A')     
            elif char == 'A':
                result.append('>>^A')

        prev_char = char           
    return ''.join(result)

def split_code(code):
    segments = []
    current_segment = []
    for char in code:
        current_segment.append(char)
        if char == 'A':
            segments.append(''.join(current_segment))
            current_segment = []
    return segments

def calculate_sequence_length(sequence, depth, memo):
    #print(sequence)
    for _ in range(depth+1):
        new_counts = Counter()
        for segment, count in sequence.items():
            #print('Segment:', segment)
            t = transform(segment)    
            segments = split_code(t)
            #print('Segments:', segments)
            for s in segments:
                new_counts[s] += count

        sequence = new_counts

    #print(sequence)
    return sum(sequence.values())


numeric_keypad = [
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    [' ', '0', 'A']
]

directional_keypad = [
    [' ', '^', 'A'],
    ['<', 'v', '>']
]

def solve_part2(codes):
    memo = {}

    numeric_graph = create_keypad_graph(numeric_keypad)
    #print('numeric_graph',numeric_graph)

    numeric_map = {char: (r, c) for r, row in enumerate(numeric_keypad) for c, char in enumerate(row) if char != ' '}
    #print('numeric_map',numeric_map)

    complexity_sum = 0

    for code in codes:
        sequences, _ = compute_sequence(numeric_graph, numeric_map['A'], code, numeric_map, True)

        mini = None
        for sequence in sequences:
            #print('Sequence:', sequence)
            segments = split_code(sequence)
            segC = Counter(segments)
            sequence_length = calculate_sequence_length(segC, 25, memo)
            #print('Length:', sequence_length)
            if not mini or sequence_length < mini:
                mini = sequence_length

        #print('Mini:', mini)
        #print('=========================')

        numeric_part = int(code[:-1])
        print(mini, numeric_part)
        complexity = mini * numeric_part
        complexity_sum += complexity

    print('Sum of complexities:', complexity_sum)


# We test here how a sequence grow to find what to put in 
# transform(...) in case of multiple choice ...

test = [ 'v<<A', '<v<A', '>^>A', '>>^A', '>^A', '^>A', '<vA', 'v<A' ]

for t in test:
    t2 = transform(t)
    print(t, ':', len(t2))
print('-------------')
for t in test:
    t2 = transform(transform(t))
    print(t, ':', len(t2))
print('-------------')
for t in test:
    t2 = transform(transform(transform(t)))
    print(t, ':', len(t2))
print('-------------')
for t in test:
    t2 = transform(transform(transform(transform(t))))
    print(t, ':', len(t2))
print('-------------')


# Part 2

codes = ['029A', '980A', '179A', '456A', '379A']
solve_part2(codes)

codes = ['964A', '140A', '413A', '670A', '593A']
solve_part2(codes)
