def gen(initial_secret, iterations=2000):
    MODULO = 16777216
    secret = initial_secret
    numbers = []
    for _ in range(iterations):
        secret = (secret ^ (secret * 64)) % MODULO
        secret = (secret ^ (secret // 32)) % MODULO
        secret = (secret ^ (secret * 2048)) % MODULO
        numbers.append(secret)
    return numbers

def find_optimal_sequence(buyers):

    def get_prices_and_changes(secret_numbers):
        prices = [num % 10 for num in secret_numbers]
        changes = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
        return prices, changes

    all_seq = {}

    for buyer in buyers:
        b_sequence = set()
        secret_numbers = gen(buyer, iterations=2000)
        prices, changes = get_prices_and_changes(secret_numbers)

        #print(prices)
        #print(changes)

        for i in range(len(changes) - 3):
            seq = tuple(changes[i:i + 4])
            # only first appearence is of interest
            if seq not in b_sequence:
                b_sequence.add(seq)
                if seq not in all_seq:
                    all_seq[seq] = []
                all_seq[seq].append(prices[i + 4])

    #print(all_seq)
    #print(len(all_seq))

    max_bananas = 0
    best_sequence = None

    # find best sequence
    for sequence, price_list in all_seq.items():
        #if sequence == [-2,1,-1,3]:
            #print(price_list)
        total_bananas = sum(price_list)
        if total_bananas > max_bananas:
            #print(price_list)
            max_bananas = total_bananas
            best_sequence = sequence

    return best_sequence, max_bananas

def solve_part2(buyers):
    best_sequence, max_bananas = find_optimal_sequence(buyers)
    print('Best sequence:', best_sequence)
    print('Max bananas:', max_bananas)


# Test
buyers = [1, 2, 3, 2024]
solve_part2(buyers)

# Real
buyers = []
with open('data/data22', 'r') as f:
    for line in f:
        initial_secret = int(line.strip())
        buyers.append(initial_secret)
solve_part2(buyers)
