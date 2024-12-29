def gen(initial_secret, iterations=2000):
    MODULO = 16777216
    secret = initial_secret
    for _ in range(iterations):
        secret = (secret ^ (secret * 64)) % MODULO
        secret = (secret ^ (secret // 32)) % MODULO
        secret = (secret ^ (secret * 2048)) % MODULO
    return secret

def solve_part1(buyers):
    total = 0
    for buyer in buyers:
        total += gen(buyer)
    return total

# Test
buyers = [1, 10, 100, 2024]
result = solve_part1(buyers)
print('Sum:', result)

# Real
buyers = []
with open('data/data22', 'r') as f:
    for line in f:
        initial_secret = int(line.strip())
        buyers.append(initial_secret)
result = solve_part1(buyers)
print('Sum:', result)
