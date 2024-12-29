from collections import defaultdict

# https://fr.wikipedia.org/wiki/Algorithme_de_Bron-Kerbosch
#
# algorithme Bron-Kerbosch(R, P, X)
#    si P et X sont vides alors
#        déclarer que R est une clique maximale
#    pour tout sommet v dans P faire
#        Bron-Kerbosch(R ⋃ {v}, P ⋂ N(v), X ⋂ N(v))
#        P := P \ {v}
#        X := X ⋃ {v}
#
# Bron-Kerbosch(∅, V, ∅) //appel initial
def bron_kerbosch(graph, r, p, x, largest_clique):
    if not p and not x:
        if len(r) > len(largest_clique[0]):
            largest_clique[0] = r
        return

    for node in list(p):
        neighbors = graph[node]
        bron_kerbosch(
            graph,
            r.union([node]),
            p.intersection(neighbors),
            x.intersection(neighbors),
            largest_clique
        )
        p.remove(node)
        x.add(node)

def solve_part2(data):
    graph = defaultdict(set)
    for line in data.splitlines():
        a, b = line.split('-')
        graph[a].add(b)
        graph[b].add(a)

    largest_clique = [set()]
    nodes = set(graph.keys())
    bron_kerbosch(graph, set(), nodes, set(), largest_clique)

    password = ','.join(sorted(largest_clique[0]))    
    print('Password :', password)


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
solve_part2(data)

# Real
data = open('data/data23', 'r').read().strip()
solve_part2(data)

