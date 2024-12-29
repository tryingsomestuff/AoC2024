from collections import defaultdict

DISPLAY = False

def find_triangles_with_t(input_data):
    graph = defaultdict(set)
    for line in input_data.splitlines():
        a, b = line.split('-')
        graph[a].add(b)
        graph[b].add(a)

    triangles = set()
    for node in graph:
        for neighbor in graph[node]:
            common_neighbors = graph[node].intersection(graph[neighbor])
            for common in common_neighbors:
                triangle = tuple(sorted([node, neighbor, common]))
                triangles.add(triangle)

    triangles_with_t = [triangle for triangle in triangles if any(node.startswith('t') for node in triangle)]
    return triangles_with_t

def solve_part1(data):
    triangles_with_t = find_triangles_with_t(data)
    if DISPLAY: 
        print("Triangles with a 't' node:")
        for triangle in triangles_with_t:
            print(triangle)
    print('\nCount:', len(triangles_with_t))    

# Test
data = '''kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn'''
solve_part1(data)

# Real
data = open('data/data23', 'r').read().strip()
solve_part1(data)
