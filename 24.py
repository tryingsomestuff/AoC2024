from collections import deque
import pydot
import random
import re

def parse_input(input_file):
    with open(input_file, 'r') as file:
        lines = file.read().strip().split('\n')
    split_index = lines.index('')
    input_values = lines[:split_index]
    gate_connections = lines[split_index + 1:]

    return input_values, gate_connections

def get_wires_and_gates(input_values, gate_connections):
    wire_values = {}
    gates = deque()
    dependencies = {}

    for line in input_values:
        wire, value = line.split(': ')
        wire_values[wire] = int(value)

    for connection in gate_connections:
        match = re.match(r"(\w+) (AND|OR|XOR) (\w+) -> (\w+)", connection)
        if match:
            in1, operation, in2, out = match.groups()
            gates.append((in1, operation, in2, out))
            dependencies[out] = (in1, operation, in2)

    return wire_values, gates, dependencies

def simulate(wires, gates):
    # we need to copy here ...
    wire_values = wires.copy()
    pending = gates.copy()

    while pending:
        in1, operation, in2, out = pending.popleft()

        if in1 in wire_values and in2 in wire_values:
            val1, val2 = wire_values[in1], wire_values[in2]

            if operation == 'AND':
                wire_values[out] = val1 & val2
            elif operation == 'OR':
                wire_values[out] = val1 | val2
            elif operation == 'XOR':
                wire_values[out] = val1 ^ val2
        else:
            pending.append((in1, operation, in2, out))

    z_wires = {wire: value for wire, value in wire_values.items() if wire.startswith('z')}
    binary_number = ''.join(str(z_wires[f'z{i:02}']) for i in range(len(z_wires)))
    # LSB is at the end, so we need to reverse the string
    binary_number = binary_number[::-1]
    return int(binary_number, 2), wire_values

# something to identify the dependencies of a specific output, not used at the end ...
def get_dependencies(wire, dependencies):
    if wire not in dependencies:
        return set()
    in1, _, in2 = dependencies[wire]
    return {wire} | get_dependencies(in1, dependencies) | get_dependencies(in2, dependencies)


# Part 1

input_values, gate_connections = parse_input('data/data24')
wire_values, gates, dependencies = get_wires_and_gates(input_values, gate_connections)
#print(wire_values)
#print(gates)
#print(dependencies)
result, output_wire_values = simulate(wire_values, gates)
print('Decimal output:', result)


# Part 2

#z_wires = {wire: value for wire, value in output_wire_values.items() if wire.startswith('z')}
#print(z_wires)
#for wire in z_wires:
    #print(wire, get_dependencies(wire, dependencies))

def loop(n, gates):
    wire_values = {}

    #input
    for i in range(45):
        if i < n:
            wire_values[f'x{i:02}'] = 1#random.randint(0, 1)
            wire_values[f'y{i:02}'] = 1#random.randint(0, 1)
        else:
            wire_values[f'x{i:02}'] = 0
            wire_values[f'y{i:02}'] = 0

    # LSB is at the end, so we need to reverse the string
    x_binary = ''.join(str(wire_values[f'x{i:02}']) for i in range(45))[::-1]
    print('x', x_binary)
    # LSB is at the end, so we need to reverse the string
    y_binary = ''.join(str(wire_values[f'y{i:02}']) for i in range(45))[::-1]
    print('y', y_binary)
    x_int = int(x_binary, 2)
    print('x_int', x_int)
    y_int = int(y_binary, 2)
    print('y_int', y_int)

    z_int = x_int + y_int
    print('z_int', z_int)
    print('z_bin', bin(z_int))
    z_binary = bin(z_int)[2:].zfill(46)  # Removing the '0b' prefix and padding to 46 bits
    print('z_expected', z_binary)
    # LSB is at the end, so we need to reverse the order
    z_expected = {f'z{i:02}': int(z_binary[45-i]) for i in range(46)}

    #print(wire_values)
    #print('expected:', dict(sorted(z_expected.items())))

    result, output_wire_values = simulate(wire_values, gates)
    z_result = ''.join(str(output_wire_values[f'z{i:02}']) for i in range(46))[::-1]
    print('Binary result:', z_result)
    print('Decimal result:', result)

    z_wires = {wire: value for wire, value in output_wire_values.items() if wire.startswith('z')}
    #print('Z :', dict(sorted(z_wires.items())))

    bad_wires = []
    #good_wires = []
    for wire in z_wires:
        #print(wire, z_wires[wire], z_expected[wire])
        if z_wires[wire] != z_expected[wire]:
            bad_wires.append(wire)  
        #else:  
            #good_wires.append(wire)

    #for wire in bad_wires:
        #bad_deps = get_dependencies(wire, dependencies)

    #for wire in good_wires:
        #good_deps = get_dependencies(wire, dependencies)

    print('bad_wires:', bad_wires)
    #print(dict(sorted(output_wire_values.items())))
    #print('good_wires:', good_wires)

    print('=========================')

print('######################')


def col(s):
    if s.startswith('z'):
        return 'red'
    if s.startswith('x'):
        return 'green'            
    if s.startswith('y'):
        return 'green'            
    if s.startswith('XOR'):
        return 'orange'            
    if s.startswith('AND'):
        return 'blue'            
    if s.startswith('OR'):
        return 'purple'   
    return 'black'         

def to_graph(gates):
    output = ''
    output += 'strict digraph {\n'
    for gate in gates:
        n1, op, n2, out = gate
        output += f'  {n1} [color={col(n1)}, shape=box]\n'
        output += f'  {n2} [color={col(n2)}, shape=box]\n'
        output += f'  {out} [color={col(out)}, shape=box]\n'
        output += f'  {n1} -> {out} [label={op} color={col(op)}]\n'
        output += f'  {n2} -> {out} [label={op} color={col(op)}]\n'
    output += '}'
    return output

def swap_gate(gates, i, j):
    new_gates = deque()
    found = 0
    for gate in gates:
        n1, op, n2, out = gate
        # change the output of the gate
        if out == i:
            out = j
            found += 1
        elif out == j:    
            out = i
            found += 1
        # or change the inputs of the gate
        #if n1 == i:
            #n1 = j
            #found += 1
        #elif n1 == j:
            #n1 = i
            #found += 1  
        #if n2 == i:
            #n2 = j
            #found += 1
        #elif n2 == j:
            #n2 = i
            #found += 1  
        new_gates.append((n1, op, n2, out))
    print('found', found)
    return new_gates

import os
if not os.path.exists('output/24/'):
    os.makedirs('output/24/')

# plot the graph
dot_str = to_graph(gates) 
pydot_graph = pydot.graph_from_dot_data(dot_str)
pydot_graph[0].write_png('output/24/graph.png')

# Assuming this is all just a 44bits full adder with carry
# this was found looking at the graph starting by the first occurence 
# of bad_wires found in the loop()
to_swap = [('z05', 'frn'), ('vtj','wnf'), ('z21', 'gmq'), ('z39', 'wtt') ] 

# build the fixed graph 
# and fill the list of the wires to swap sorted in alphabetical order
l = []
for i,j in to_swap:
    l.append(i)
    l.append(j)
    print('swapping', i, j) 
    gates = swap_gate(gates, i, j)

# plot the fixed graph
dot_str = to_graph(gates) 
pydot_graph = pydot.graph_from_dot_data(dot_str)
pydot_graph[0].write_png('output/24/graph_swapped.png')

# Testing for bad z outputs
for i in range(45):
    loop(i, gates) 
# Look for the first not empty 'bad_wires' in the output
# and have a look at the graph plotted to guess the fix

print('Answer:', ','.join(sorted(l)))
