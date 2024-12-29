from collections import deque

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

def bfs(graph, start, goal, use_cache):
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

# Too naive ...
def compute_sequence(keypad_graph, start_pos, code, keypad_map, use_cache):
    if debug: print('---compute_sequence', start_pos, code)
    #if debug: print('---compute_sequence', keypad_graph)
    current_pos = start_pos
    all_sequences = [[]]

    for char in code:
        target_pos = keypad_map[char]
        if debug: print('---compute_sequence', char, target_pos, current_pos)
        all_paths = bfs(keypad_graph, current_pos, target_pos, use_cache)
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

def split_code(code):
    segments = []
    current_segment = []
    for char in code:
        current_segment.append(char)
        if char == 'A':
            segments.append(''.join(current_segment))
            current_segment = []
    return segments

# a first optimization, using a memo for each segment
# and possibly a cache for the BFS
# the bfs memory is bounded as the graph is small 
# the segments memory can grow bigger, use with care
def compute_sequence_opt(keypad_graph, start_pos, code, keypad_map, use_cache):
    global memo_pad

    segments = split_code(code)

    current_pos = start_pos
    all_sequences = [[]]

    for segment in segments:
        if segment in memo_pad:
            #print('match', segment)
            all_sequences_segment, current_pos_segment = memo_pad[segment]
        else:
            all_sequences_segment = [[]]
            for char in segment:
                target_pos = keypad_map[char]
                all_paths = bfs(keypad_graph, current_pos, target_pos, use_cache)
                all_path_commands = [path_to_commands(path) for path in all_paths]
                all_sequences_segment = [
                    existing_sequence + new_commands
                    for existing_sequence in all_sequences_segment
                    for new_commands in all_path_commands
                ]
                current_pos = target_pos

            memo_pad[segment] = (all_sequences_segment, current_pos)

        all_sequences = [
            existing_sequence + new_sequence
            for existing_sequence in all_sequences
            for new_sequence in all_sequences_segment
        ]

    return all_sequences, current_pos

# Another optimization using the BFS cache and 
# a divide-and-conquer / dichotomy mindset
# and a memo for segments of various size < 64 characters
# the bfs memory is bounded as the graph is small 
# the segments memory can grow a lot bigger, use with care
def compute_sequence_opt2(keypad_graph, start_pos, code, keypad_map, use_cache):
    global memo_pad

    def compute_with_split(code):
        #print('code', code)
        if code in memo_pad:
            return memo_pad[code]

        segments = split_code(code)
        #print('segments', segments)

        if len(segments) > 1:
            mid = len(segments) // 2
            part1 = segments[:mid]
            part2 = segments[mid:]

            #print('part1', part1)
            #print('part2', part2)

            part1_result = compute_with_split(''.join(part1))
            part2_result = compute_with_split(''.join(part2))

            if not part1_result:
                part1_result = compute_sequence_opt_direct(keypad_graph, start_pos, ''.join(part1), keypad_map, use_cache)
            if not part2_result:
                part2_result = compute_sequence_opt_direct(keypad_graph, start_pos, ''.join(part2), keypad_map, use_cache)

            #print('hit', part1, part2)
            all_sequences = [
                seq1 + seq2
                for seq1 in part1_result[0]
                for seq2 in part2_result[0]
            ]

            if len(code) < 64:
                memo_pad[code] = (all_sequences, part2_result[1])

            return all_sequences, part2_result[1]

        return compute_sequence_opt_direct(keypad_graph, start_pos, code, keypad_map, use_cache)

    # same as the naive version with a cache for segments and BFS
    def compute_sequence_opt_direct(keypad_graph, start_pos, code, keypad_map, use_cache):
        segments = split_code(code)
        current_pos = start_pos
        all_sequences = [[]]

        for segment in segments:
            if segment in memo_pad:
                all_sequences_segment, current_pos_segment = memo_pad[segment]
            else:
                all_sequences_segment = [[]]
                for char in segment:
                    target_pos = keypad_map[char]
                    all_paths = bfs(keypad_graph, current_pos, target_pos, use_cache)
                    all_path_commands = [path_to_commands(path) for path in all_paths]
                    all_sequences_segment = [
                        existing_sequence + new_commands
                        for existing_sequence in all_sequences_segment
                        for new_commands in all_path_commands
                    ]
                    current_pos = target_pos

                memo_pad[segment] = (all_sequences_segment, current_pos)

            all_sequences = [
                existing_sequence + new_sequence
                for existing_sequence in all_sequences
                for new_sequence in all_sequences_segment
            ]

        if len(code) < 64:
            memo_pad[code] = (all_sequences, current_pos)

        return all_sequences, current_pos

    return compute_with_split(code)

# Search taking current level into account
# First level is a numeric pad, while others are directional pad
def compute_recursive_sequence(sequences, level, max_level, numeric_graph, directional_graph, start_position_numeric, start_position_directional, code, numeric_map, directional_map):
    if debug: print('level', level, 'input', code)
    
    sequences[level].add(code)
    
    if level == 0:
        if debug: print('start', start_position_numeric[0])
        all_sequences, start_position_numeric[0] = compute_sequence_opt(numeric_graph, start_position_numeric[0], code, numeric_map, False)
        all_sequences = [''.join(sequence) for sequence in all_sequences]
        if debug: print('all_sequences', all_sequences)
        all_recursive_sequences = []
        for sequence in all_sequences:
            if debug: print(f'level {level}', sequence, f'going to level {level+1}')
            all_recursive_sequences.append(compute_recursive_sequence(sequences, level+1, max_level, numeric_graph, directional_graph, start_position_numeric, start_position_directional, sequence, numeric_map, directional_map))
        return all_recursive_sequences
    
    if level != max_level:
        if debug: print('start', start_position_directional[0])
        all_sequences, start_position_directional[0] = compute_sequence_opt2(directional_graph, start_position_directional[0], code, directional_map, True)
        all_sequences = [''.join(sequence) for sequence in all_sequences]
        if debug: print('all_sequences', all_sequences)
        all_recursive_sequences = []
        for sequence in all_sequences:
            if debug: print(f'level {level}', sequence, f'going to level {level+1}')
            all_recursive_sequences.append(compute_recursive_sequence(sequences, level+1, max_level, numeric_graph, directional_graph, start_position_numeric, start_position_directional, sequence, numeric_map, directional_map))
        return all_recursive_sequences

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

# This is slow and dummy ...
def solve_part1(codes):
    numeric_graph = create_keypad_graph(numeric_keypad)
    #print('numeric_graph',numeric_graph)
    directional_graph = create_keypad_graph(directional_keypad)
    #print('directional_graph',directional_graph)

    numeric_map = {char: (r, c) for r, row in enumerate(numeric_keypad) for c, char in enumerate(row) if char != ' '}
    #print('numeric_map',numeric_map)
    directional_map = {char: (r, c) for r, row in enumerate(directional_keypad) for c, char in enumerate(row) if char != ' '}
    #print('directional_map',directional_map)

    start_position_numeric = [numeric_map['A']]
    start_position_directional = [directional_map['A']]

    complexity_sum = 0

    for code in codes:
        print('code', code)
        sequences = { 0: set(), 1: set(), 2: set(), 3: set() }
        compute_recursive_sequence(sequences, 0, 3, numeric_graph, directional_graph, start_position_numeric, start_position_directional, code, numeric_map, directional_map)
        sequence_length = 0
        for level in sequences:
            #print(f'level {level}', len(sequences[level]))
            sequence_length = len(min(sequences[level], key=len))
            #print(f'level {level}', sequence_length)

        numeric_part = int(code[:-1])
        #print(sequence_length, numeric_part)
        complexity = sequence_length * numeric_part
        complexity_sum += complexity

    print('Sum of complexities:', complexity_sum)

codes = ['029A', '980A', '179A', '456A', '379A']
solve_part1(codes)

codes = ['964A', '140A', '413A', '670A', '593A']
solve_part1(codes)