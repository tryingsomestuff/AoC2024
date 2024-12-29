from collections import Counter

def read(fn):
    l, r = [], []
    with open(fn, 'r') as f:
        for line in f:
            a, b = map(int, line.split())
            l.append(a)
            r.append(b)
    return l, r

def calc_dist(l, r):
    return sum(abs(a - b) for a, b in zip(sorted(l), sorted(r)))

def calc_sim(l, r):
    rc = Counter(r)
    return sum(x * rc[x] for x in l)

# Test
l = [3, 4, 2, 1, 3, 3]
r = [4, 3, 5, 3, 9, 3]
print(f'Total distance: {calc_dist(l, r)}')
print(f'Similarity score: {calc_sim(l, r)}')

# Real
l, r = read('data/data01')
print(f'Total distance: {calc_dist(l, r)}')
print(f'Similarity score: {calc_sim(l, r)}')