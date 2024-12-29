def read(fn):
    with open(fn, 'r') as file:
        lines = file.read().strip().split('\n')

    locks = []
    keys = []
    schema = []

    for line in lines:
        if line.strip():
            schema.append(line)
        else:
            if schema:
                if '#' in schema[0]:
                    locks.append(schema)
                elif '#' in schema[-1]:
                    keys.append(schema)
                schema = []

    if schema:
        if '#' in schema[0]:
            locks.append(schema)
        elif '#' in schema[-1]:
            keys.append(schema)

    return locks, keys

# convert schema to heights
def parse_schema(schema):
    columns = list(zip(*schema))
    heights = []
    for col in columns:
        height = col.count('#')
        heights.append(height)
    return heights

def fits(lock, key):
    for lock_height, key_height in zip(lock, key):
        if lock_height + key_height > 7:
            return False
    return True

def count_pairs(locks, keys):
    fitting_pairs = 0
    for lock in locks:
        for key in keys:
            if fits(lock, key):
                fitting_pairs += 1
    return fitting_pairs

def solve_part1(filename):

    locks_schemas, keys_schemas = read(filename)
    #print(locks_schemas)
    #print(keys_schemas)

    locks = [parse_schema(lock) for lock in locks_schemas]
    keys = [parse_schema(key) for key in keys_schemas]
    #print(locks)
    #print(keys)

    result = count_pairs(locks, keys)
    print(f'Number of fitting lock/key pairs: {result}')


solve_part1('data/data25_sample')

solve_part1('data/data25')
