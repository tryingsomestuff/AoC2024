from collections import Counter

def simulate_blinks(initial_stones, blinks):
    stone_counts = Counter(initial_stones)

    for _ in range(blinks):
        new_counts = Counter()
        for stone, count in stone_counts.items():
            if stone == 0:
                new_counts[1] += count
            elif len(str(stone)) % 2 == 0:
                half = len(str(stone)) // 2
                left = int(str(stone)[:half])
                right = int(str(stone)[half:])
                new_counts[left] += count
                new_counts[right] += count
            else:
                new_counts[stone * 2024] += count
        #print(stone_counts)
        #print(new_counts)
        stone_counts = new_counts
        #print('===============')

    return sum(stone_counts.values())

initial_stones = [1117, 0, 8, 21078, 2389032, 142881, 93, 385]

# Part 1
blinks = 25
result = simulate_blinks(initial_stones, blinks)
print(f'Number of stones after {blinks} blinks: {result}')

# Part 2
blinks = 75
result = simulate_blinks(initial_stones, blinks)
print(f'Number of stones after {blinks} blinks: {result}')