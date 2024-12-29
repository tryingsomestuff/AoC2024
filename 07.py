from itertools import product

def match(t, ns):
    n = len(ns)
    # build all possible combinaison
    ops = list(product(['+', '*'], repeat=n-1))
    # try them ...
    for o in ops:
        e = (n-1)*'(' + str(ns[0])
        # build the expression
        for i in range(n - 1):
            e += o[i] + str(ns[i + 1]) + ')'
        # verify
        if eval(e) == t:
            #print(e, t)
            return True
    return False

def solve_part1(eqs):
    s = 0
    for e in eqs:
        t, ns = e[0], e[1:]
        if match(t, ns):
            s += t
    return s

def read(fn):
    eqs = []
    with open(fn, 'r') as f:
        for l in f:
            t, ns = l.split(':')
            t = int(t.strip())
            ns = list(map(int, ns.split()))
            eqs.append([t] + ns)
    return eqs

def concat(a, b):
    return int(str(a) + str(b))

def match2(t, nums):
    n = len(nums)
    # build all possible combinaison
    ops = list(product(['+', '*', '||'], repeat=n-1))
    # try them ...
    for op in ops:
        cur = nums[0]
        # build the expression
        for i in range(n - 1):
            if op[i] == '+':
                cur += nums[i + 1]
            elif op[i] == '*':
                cur *= nums[i + 1]
            elif op[i] == '||':
                cur = concat(cur, nums[i + 1])
        # verify
        if cur == t:
            return True
    return False

def solve_part2(eqs):
    s = 0
    for e in eqs:
        t, ns = e[0], e[1:]
        if match2(t, ns):
            s += t
    return s

eqs = read('data/data07_sample')
print('Total sample:', solve_part1(eqs))
print('Total sample:', solve_part2(eqs))

eqs = read('data/data07')
print('Total real:', solve_part1(eqs))
print('Total real:', solve_part2(eqs))
