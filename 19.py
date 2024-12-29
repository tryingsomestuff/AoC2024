# Part 1

def can(design, patterns, memo):
    if design in memo:
        return memo[design]

    if not design:
        return True

    for p in patterns:
        if design.startswith(p):
            if can(design[len(p):], patterns, memo):
                memo[design] = True
                return True

    memo[design] = False
    return False

def count_designs(patterns, designs):
    memo = {}
    count = 0
    for design in designs:
        if can(design, patterns, memo):
            count += 1
    return count

# Part 2

def count_arrangements(design, patterns, memo):
    if design in memo:
        return memo[design]

    if not design:
        return 1

    sum = 0
    for p in patterns:
        if design.startswith(p):
            sum += count_arrangements(design[len(p):], patterns, memo)

    memo[design] = sum
    return sum

def total_arrangements(patterns, designs):
    memo = {}
    memoC = {}
    sum = 0
    for design in designs:
        if can(design, patterns, memoC):
            sum += count_arrangements(design, patterns, memo)
    return sum

# Test
patterns = ['r', 'wr', 'b', 'g', 'bwu', 'rb', 'gb', 'br']
designs = [
    'brwrr',
    'bggr',
    'gbbr',
    'rrbgbr',
    'ubwu',
    'bwurrg',
    'brgr',
    'bbrgwb',
]
possible_count = count_designs(patterns, designs)
print(f'Number of designs: {possible_count}')

count = total_arrangements(patterns, designs)
print(f'Number of arrangements: {count}')

def read(fn):
    with open(fn, 'r') as f:
        lines = f.read().strip().split('\n')
        patterns = lines[0].split(', ')
        designs = lines[1:]
    for x in designs[:]:
        if not x.strip():
            designs.remove(x)        
    return patterns, designs

# Real
patterns, designs = read('data/data19')
possible_count = count_designs(patterns, designs)
print(f'Number of designs: {possible_count}')

count = total_arrangements(patterns, designs)
print(f'Number of arrangements: {count}')