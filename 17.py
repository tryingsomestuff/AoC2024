display = False

def computer(initial_a, initial_b, initial_c, program):
    A = initial_a
    B = initial_b
    C = initial_c

    ip = 0

    output = []

    def get_combo_value(operand):
        if operand <= 3:
            return operand
        elif operand == 4:
            return A
        elif operand == 5:
            return B
        elif operand == 6:
            return C
        else:
            raise ValueError('Invalid combo operand')

    while ip < len(program):
        opcode = program[ip]
        operand = program[ip + 1]

        if opcode == 0:  
            if display: print(f'adv: A //= 2^operand   A:{A} B:{B}  C:{C}  op:{operand}')
            denominator = 2 ** get_combo_value(operand)
            A //= denominator
        elif opcode == 1:
            if display: print(f'bxl: B ^= operand (literal)   A:{A} B:{B}  C:{C}  op:{operand}')
            B ^= operand
        elif opcode == 2:
            if display: print(f'bst: B = combo_operand % 8   A:{A} B:{B}  C:{C}  op:{operand}')
            B = get_combo_value(operand) % 8
        elif opcode == 3:
            if display: print(f'jnz: if A != 0, jump to operand (literal)   A:{A} B:{B}  C:{C}  op:{operand}')
            if A != 0:
                ip = operand
                continue
        elif opcode == 4:
            if display: print(f'bxc: B ^= C (operand ignored)   A:{A} B:{B}  C:{C}  op:{operand}')
            B ^= C
        elif opcode == 5:
            if display: print(f'out: output combo_operand % 8   A:{A} B:{B}  C:{C}  op:{operand}')
            output.append(get_combo_value(operand) % 8)
        elif opcode == 6:
            if display: print(f'bdv: B = A // (2^operand)   A:{A} B:{B}  C:{C}  op:{operand}')
            denominator = 2 ** get_combo_value(operand)
            B = A // denominator
        elif opcode == 7:
            if display: print(f'cdv: C = A // (2^operand)   A:{A} B:{B}  C:{C}  op:{operand}')
            denominator = 2 ** get_combo_value(operand)
            C = A // denominator
        else:
            raise ValueError(f'Invalid opcode {opcode}')

        ip += 2

    return output

# Part 1

# Test
initial_a = 729
initial_b = 0
initial_c = 0
program = [0, 1, 5, 4, 3, 0]

result = computer(initial_a, initial_b, initial_c, program)
print('Output:', ','.join(map(str, result)))

# Real
initial_a = 30553366
initial_b = 0
initial_c = 0
program = [2,4,1,1,7,5,4,7,1,4,0,3,5,5,3,0]

result = computer(initial_a, initial_b, initial_c, program)
print('Output:', ','.join(map(str, result)))

# Part 2

# Execution trace of the given program

'''
bst: B = combo_operand % 8   A:30553366 B:0  C:0  op:4
bxl: B ^= operand (literal)   A:30553366 B:6  C:0  op:1
cdv: C = A // (2^operand)   A:30553366 B:7  C:0  op:5
bxc: B ^= C (operand ignored)   A:30553366 B:7  C:238698  op:7
bxl: B ^= operand (literal)   A:30553366 B:238701  C:238698  op:4
adv: A //= 2^operand   A:30553366 B:238697  C:238698  op:3
out: output combo_operand % 8   A:3819170 B:238697  C:238698  op:5
jnz: if A != 0, jump to operand (literal)   A:3819170 B:238697  C:238698  op:0
bst: B = combo_operand % 8   A:3819170 B:238697  C:238698  op:4
bxl: B ^= operand (literal)   A:3819170 B:2  C:238698  op:1
cdv: C = A // (2^operand)   A:3819170 B:3  C:238698  op:5
bxc: B ^= C (operand ignored)   A:3819170 B:3  C:477396  op:7
bxl: B ^= operand (literal)   A:3819170 B:477399  C:477396  op:4
adv: A //= 2^operand   A:3819170 B:477395  C:477396  op:3
out: output combo_operand % 8   A:477396 B:477395  C:477396  op:5
jnz: if A != 0, jump to operand (literal)   A:477396 B:477395  C:477396  op:0
bst: B = combo_operand % 8   A:477396 B:477395  C:477396  op:4
bxl: B ^= operand (literal)   A:477396 B:4  C:477396  op:1
cdv: C = A // (2^operand)   A:477396 B:5  C:477396  op:5
bxc: B ^= C (operand ignored)   A:477396 B:5  C:14918  op:7
bxl: B ^= operand (literal)   A:477396 B:14915  C:14918  op:4
adv: A //= 2^operand   A:477396 B:14919  C:14918  op:3
out: output combo_operand % 8   A:59674 B:14919  C:14918  op:5
jnz: if A != 0, jump to operand (literal)   A:59674 B:14919  C:14918  op:0
bst: B = combo_operand % 8   A:59674 B:14919  C:14918  op:4
bxl: B ^= operand (literal)   A:59674 B:2  C:14918  op:1
cdv: C = A // (2^operand)   A:59674 B:3  C:14918  op:5
bxc: B ^= C (operand ignored)   A:59674 B:3  C:7459  op:7
bxl: B ^= operand (literal)   A:59674 B:7456  C:7459  op:4
adv: A //= 2^operand   A:59674 B:7460  C:7459  op:3
out: output combo_operand % 8   A:7459 B:7460  C:7459  op:5
jnz: if A != 0, jump to operand (literal)   A:7459 B:7460  C:7459  op:0
bst: B = combo_operand % 8   A:7459 B:7460  C:7459  op:4
bxl: B ^= operand (literal)   A:7459 B:3  C:7459  op:1
cdv: C = A // (2^operand)   A:7459 B:2  C:7459  op:5
bxc: B ^= C (operand ignored)   A:7459 B:2  C:1864  op:7
bxl: B ^= operand (literal)   A:7459 B:1866  C:1864  op:4
adv: A //= 2^operand   A:7459 B:1870  C:1864  op:3
out: output combo_operand % 8   A:932 B:1870  C:1864  op:5
jnz: if A != 0, jump to operand (literal)   A:932 B:1870  C:1864  op:0
bst: B = combo_operand % 8   A:932 B:1870  C:1864  op:4
bxl: B ^= operand (literal)   A:932 B:4  C:1864  op:1
cdv: C = A // (2^operand)   A:932 B:5  C:1864  op:5
bxc: B ^= C (operand ignored)   A:932 B:5  C:29  op:7
bxl: B ^= operand (literal)   A:932 B:24  C:29  op:4
adv: A //= 2^operand   A:932 B:28  C:29  op:3
out: output combo_operand % 8   A:116 B:28  C:29  op:5
jnz: if A != 0, jump to operand (literal)   A:116 B:28  C:29  op:0
bst: B = combo_operand % 8   A:116 B:28  C:29  op:4
bxl: B ^= operand (literal)   A:116 B:4  C:29  op:1
cdv: C = A // (2^operand)   A:116 B:5  C:29  op:5
bxc: B ^= C (operand ignored)   A:116 B:5  C:3  op:7
bxl: B ^= operand (literal)   A:116 B:6  C:3  op:4
adv: A //= 2^operand   A:116 B:2  C:3  op:3
out: output combo_operand % 8   A:14 B:2  C:3  op:5
jnz: if A != 0, jump to operand (literal)   A:14 B:2  C:3  op:0
bst: B = combo_operand % 8   A:14 B:2  C:3  op:4
bxl: B ^= operand (literal)   A:14 B:6  C:3  op:1
cdv: C = A // (2^operand)   A:14 B:7  C:3  op:5
bxc: B ^= C (operand ignored)   A:14 B:7  C:0  op:7
bxl: B ^= operand (literal)   A:14 B:7  C:0  op:4
adv: A //= 2^operand   A:14 B:3  C:0  op:3
out: output combo_operand % 8   A:1 B:3  C:0  op:5
jnz: if A != 0, jump to operand (literal)   A:1 B:3  C:0  op:0
bst: B = combo_operand % 8   A:1 B:3  C:0  op:4
bxl: B ^= operand (literal)   A:1 B:1  C:0  op:1
cdv: C = A // (2^operand)   A:1 B:0  C:0  op:5
bxc: B ^= C (operand ignored)   A:1 B:0  C:1  op:7
bxl: B ^= operand (literal)   A:1 B:1  C:1  op:4
adv: A //= 2^operand   A:1 B:5  C:1  op:3
out: output combo_operand % 8   A:0 B:5  C:1  op:5
jnz: if A != 0, jump to operand (literal)   A:0 B:5  C:1  op:0
Output: 1,3,7,4,6,4,2,3,5
'''

# op is always 4 1 5 7 4 3 5 0
# This is a loop !

'''
bst: B = combo_operand % 8   A:30553366 B:0  C:0  op:4                B = A % 8
bxl: B ^= operand (literal)   A:30553366 B:6  C:0  op:1               B = B ^ 0x00000001
cdv: C = A // (2^operand)   A:30553366 B:7  C:0  op:5                 C = A / 32
bxc: B ^= C (operand ignored)   A:30553366 B:7  C:238698  op:7        B = B XOR C
bxl: B ^= operand (literal)   A:30553366 B:238701  C:238698  op:4     B = B XOR 0x00000100
adv: A //= 2^operand   A:30553366 B:238697  C:238698  op:3            A = A / 8
out: output combo_operand % 8   A:3819170 B:238697  C:238698  op:5    display B%8
'''

# Let's 'reverse' that ...

def generate(program, output):
    if not output:
        return [0]

    results = []
    for ah in generate(program, output[1:]):
        for al in range(8):
            a = ah * 8 + al
            if computer(a, 0, 0, program) == output:
                results.append(a)
    return results

results = generate(program, program)
print(min(results))
