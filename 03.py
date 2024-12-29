import re

def solve_part1(mem):
    return sum(int(x) * int(y) for x, y in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", mem))

def solve_part2(c):
    p1, p2, p3 = r"mul\((\d{1,3}),(\d{1,3})\)", r"do\(\)", r"don't\(\)"
    e, s, i = True, 0, 0
    while i < len(c):
        m1, m2, m3 = re.match(p1, c[i:]), re.match(p2, c[i:]), re.match(p3, c[i:])
        if m1:
            if e: s += int(m1[1]) * int(m1[2])
            i += len(m1[0])
        elif m2:
            e = True
            i += len(m2[0])
        elif m3:
            e = False
            i += len(m3[0])
        else:
            i += 1
    return s

def read(fn):
    with open(fn, 'r') as file:
        lines = file.read().strip().split('\n')
    return lines

# Test
input = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""

result = solve_part1(input)
print(result)

result = solve_part2(input)
print(result)

# Real
input = ''.join(read('data/data03'))

result = solve_part1(input)
print(result)

result = solve_part2(input)
print(result)