from collections import defaultdict
from collections import deque

def verify(u, r):
    p = defaultdict(set)
    for a, b in r:
        #print(a,b)
        p[b].add(a)
    #print('==========')

    idx = {x: i for i, x in enumerate(u)}
    #print(idx)
    #print('==========')

    for b in p:
        #print(b)
        for a in p[b]:
            # is the order ok
            if a in idx and b in idx and idx[a] > idx[b]:
                #print('wrong',a,b)
                return False
    return True

def solve_part1(r, u):
    # read data
    r = [tuple(map(int, x.split('|'))) for x in r.strip().split('\n')]
    u = [list(map(int, x.split(','))) for x in u.strip().split('\n')]
    
    return sum(x[len(x) // 2] for x in u if verify(x, r))

# Kahn's algorithm for topological sorting
def fix(u, r):
    g = defaultdict(set) # set of nodes that depends on key
    d = defaultdict(int) # 'in-degree' of nodes

    for x, y in r:
        if x in u and y in u:
            g[x].add(y)
            d[y] += 1
            if x not in d: d[x] = 0
            
    q = deque([n for n in u if d[n] == 0])
    s = []
    while q:
        c = q.popleft()
        s.append(c)
        for n in g[c]:
            d[n] -= 1
            if d[n] == 0: q.append(n)
    return s

def solve_part2(r_d, u_d):
    # read data
    r = [tuple(map(int, x.split('|'))) for x in r_d.strip().split('\n')]
    u = [list(map(int, x.split(','))) for x in u_d.strip().split('\n')]

    return sum(fix(e, r)[len(e) // 2] for e in u if not verify(e, r))

def read(fn):
    with open(fn, 'r') as file:
        lines = file.read().strip().split('\n\n')
    return lines

# Test
rules_data = '''
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13
'''

updates_data = '''
75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
'''

result = solve_part1(rules_data, updates_data)
print('Sum is:', result)

result = solve_part2(rules_data, updates_data)
print('Sum fixed is:', result)

# Real
[rules_data, updates_data] = read('data/data05')

result = solve_part1(rules_data, updates_data)
print('Sum is:', result)

result = solve_part2(rules_data, updates_data)
print('Sum fixed is:', result)