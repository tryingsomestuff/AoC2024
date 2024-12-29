from math import gcd
import re

def parse(file_path):
    results = []
    with open(file_path, 'r') as file:
        data = file.read()
        
    blocks = data.strip().split('\n\n')
    
    for block in blocks:
        match_a = re.search(r"Button A: X\+(\d+), Y\+(\d+)", block)
        match_b = re.search(r"Button B: X\+(\d+), Y\+(\d+)", block)
        match_prize = re.search(r"Prize: X=(\d+), Y=(\d+)", block)
        
        if match_a and match_b and match_prize:
            result = {
                'A': {'X': int(match_a.group(1)), 'Y': int(match_a.group(2))},
                'B': {'X': int(match_b.group(1)), 'Y': int(match_b.group(2))},
                'Prize': {'X': int(match_prize.group(1)), 'Y': int(match_prize.group(2))}
            }
            results.append(result)
    
    return results

def det(ax, ay, bx, by):
    return ax * by - ay * bx;

def solve_one(X_A, Y_A, X_B, Y_B, X_prize, Y_prize):

    i = int(det(X_prize, Y_prize, X_B, Y_B) / det(X_A, Y_A, X_B, Y_B))
    j = int(det(X_A, Y_A, X_prize, Y_prize) / det(X_A, Y_A, X_B, Y_B))

    #print(i,j)

    if (i >= 0 and j >= 0 and X_A * i + X_B * j == X_prize and Y_A * i + Y_B * j == Y_prize):
        return 3 * i + j
    else:
        return 0

def solve_part2(machines):
    total_prizes = 0
    total_tokens = 0

    for machine in machines:
        #print(machine)
        X_A, Y_A = machine['A']['X'], machine['A']['Y']
        X_B, Y_B = machine['B']['X'], machine['B']['Y']
        X_prize = machine['Prize']['X'] + 10**13
        Y_prize = machine['Prize']['Y'] + 10**13

        cost = solve_one(X_A, Y_A, X_B, Y_B, X_prize, Y_prize)
        if cost != 0:
            total_prizes += 1
            total_tokens += cost

    return total_prizes, total_tokens


data = parse('data/data13_sample')
prizes, tokens = solve_part2(data)
print(f'Total prizes won: {prizes}')
print(f'Total tokens spent: {tokens}')


data = parse('data/data13')
prizes, tokens = solve_part2(data)
print(f'Total prizes won: {prizes}')
print(f'Total tokens spent: {tokens}')