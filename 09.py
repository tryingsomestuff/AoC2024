def solve_part1(input_string):
    on_disk = []
    id = 0
    k = 0

    for char in input_string:
        n = int(char)
        if (k % 2) == 0:
            sid = str(id)
            repeated_sid = n * [sid]
            on_disk.extend(repeated_sid)
            id += 1
        else:
            on_disk.extend(n * ['.'])
        k += 1

    #print(on_disk)

    # a two pointer thing ...
    left = 0
    right = len(on_disk) - 1
    while left < right:
        # left most dot
        while left < len(on_disk) and on_disk[left] != '.':
            left += 1

        # right most digit
        while right >= 0 and not on_disk[right].isdigit():
            right -= 1

        if left < right:
            on_disk[left], on_disk[right] = on_disk[right], on_disk[left]
            left += 1
            right -= 1
        else:
            break

    #print(on_disk)
    
    # remove dots (that shall be at the end only in this case ...)
    on_disk =  [i for i in on_disk if i != '.']

    def chunked_sum(s, chunk_size=10**6):
        total = 0
        for start in range(0, len(s), chunk_size):
            chunk = s[start:start + chunk_size]
            total += sum(int(char) * (start + i) for i, char in enumerate(chunk))
            #print(total)
        return total

    result = chunked_sum(on_disk)

    return result

def read(fn):
    with open(fn, 'r') as file:
        lines = file.read().strip().split('\n')
    return lines

# Test
input_string = '2333133121414131402'

result = solve_part1(input_string)
print('Result:', result)

# Real
input_string = read('data/data09')[0]

result = solve_part1(input_string)
print('Result:', result)