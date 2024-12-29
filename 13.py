
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
    
def solve_part1(machines):
    max_presses = 100
    total_prizes = 0
    total_tokens = 0

    for machine in machines:
        X_A, Y_A = machine['A']['X'], machine['A']['Y']
        X_B, Y_B = machine['B']['X'], machine['B']['Y']
        X_prize, Y_prize = machine['Prize']['X'], machine['Prize']['Y']
        
        min_cost = float('inf')
        prize_won = False
        
        for n_A in range(max_presses + 1):
            X_remaining = X_prize - n_A * X_A
            Y_remaining = Y_prize - n_A * Y_A
            
            if X_remaining % X_B == 0 and Y_remaining % Y_B == 0:
                n_B = X_remaining // X_B
                if n_B >= 0 and n_B * Y_B == Y_remaining:
                    cost = 3 * n_A + n_B
                    if cost < min_cost:
                        min_cost = cost
                        prize_won = True
        
        if prize_won:
            total_prizes += 1
            total_tokens += min_cost

    return total_prizes, total_tokens

data = parse('data/data13_sample')
prizes, tokens = solve_part1(data)
print(f'Total prizes won: {prizes}')
print(f'Total tokens spent: {tokens}')


data = parse('data/data13')
prizes, tokens = solve_part1(data)
print(f'Total prizes won: {prizes}')
print(f'Total tokens spent: {tokens}')
