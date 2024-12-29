def read(fn):
    with open(fn, 'r') as file:
        lines = file.read().strip().split('\n')
    return lines

def safe(r):
    d = [r[i + 1] - r[i] for i in range(len(r) - 1)]
    return all(-3 <= x <= -1 for x in d) or all(1 <= x <= 3 for x in d)

def safe_damp(r, damped):
    if safe(r): return True
    if damped:
        for i in range(len(r)):
            if safe(r[:i] + r[i+1:]): return True
    return False

def count_safe(d, damped = False):
    return sum(1 for r in d if safe_damp(list(map(int, r.split())), damped))

# Test
p = [
    '7 6 4 2 1', 
    '1 2 7 8 9', 
    '9 7 6 2 1', 
    '1 3 2 4 5', 
    '8 6 4 4 1', 
    '1 3 6 7 9'
]
print(f'Safe reports: {count_safe(p)}')
print(f'Safe reports: {count_safe(p, True)}')

# Real
p = read('data/data02')
print(f'Safe reports: {count_safe(p)}')
print(f'Safe reports: {count_safe(p, True)}')

