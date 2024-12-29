def parse_warehouse(warehouse_str):
    warehouse = [list(line) for line in warehouse_str.strip().split('\n')]
    robot_pos = None
    boxes = []

    for r, row in enumerate(warehouse):
        for c, char in enumerate(row):
            if char == '@':
                robot_pos = (r, c)
                warehouse[r][c] = '.'
            elif char == 'O':
                boxes.append((r, c))
                warehouse[r][c] = '.'

    return warehouse, robot_pos, boxes

def display_warehouse(warehouse, robot_pos, boxes):
    display = [row[:] for row in warehouse]
    r, c = robot_pos
    display[r][c] = '@'
    for br, bc in boxes:
        display[br][bc] = 'O'
    for row in display:
        print(''.join(row))

def move_robot(warehouse, robot_pos, boxes, moves):
    directions = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}

    #display_warehouse(warehouse, robot_pos, boxes)

    for move in moves:
        #print('=====================================')
        dr, dc = directions[move]
        #print('direction', dr,dc)
        nr, nc = robot_pos[0] + dr, robot_pos[1] + dc

        if warehouse[nr][nc] == '#':
            #print('wall ',nr,nc)
            #display_warehouse(warehouse, robot_pos, boxes)
            continue

        cascade_path = []
        can_move = True
        if (nr, nc) in boxes:
            #print('box ',nr,nc)
            br, bc = nr + dr, nc + dc

            cascade_path = [(br, bc)]
            while True:
                cr, cc = cascade_path[-1]

                if warehouse[cr][cc] == '#':
                    cascade_path = []
                    can_move = False
                    break

                if (cr, cc) in boxes:
                    cascade_path.append((cr+dr,cc+dc))
                else:
                    break

        if can_move:
            robot_pos = (nr, nc)
            for r,c in cascade_path:
                #print('remove',r-dr,c-dc)
                boxes.remove((r-dr,c-dc))
            for r,c in cascade_path:
                #print('add',r,c)
                boxes.append((r,c))

        #display_warehouse(warehouse, robot_pos, boxes)

    return robot_pos, boxes

def calculate_gps_sum(boxes):
    return sum(100 * r + c for r, c in boxes)

def read(fn):
    with open(fn, 'r') as file:
        lines = file.read().strip().split('\n\n')
    return lines

# Mini test
warehouse_str = '''########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########'''

moves = '<^^>>>vv<v>>v<<'.replace('\n', '')

warehouse, robot_pos, boxes = parse_warehouse(warehouse_str)
robot_pos, boxes = move_robot(warehouse, robot_pos, boxes, moves)
gps_sum = calculate_gps_sum(boxes)
print('Sum of GPS coordinates:', gps_sum)

# Test
warehouse_str = '''##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########'''

moves = '''
<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
'''.replace('\n', '')

warehouse, robot_pos, boxes = parse_warehouse(warehouse_str)
robot_pos, boxes = move_robot(warehouse, robot_pos, boxes, moves)
gps_sum = calculate_gps_sum(boxes)
print('Sum of GPS coordinates:', gps_sum)

# Real
[warehouse_str, moves] = read('data/data15')
moves = moves.replace('\n', '')
warehouse, robot_pos, boxes = parse_warehouse(warehouse_str)
robot_pos, boxes = move_robot(warehouse, robot_pos, boxes, moves)
gps_sum = calculate_gps_sum(boxes)
print('Sum of GPS coordinates:', gps_sum)


# Part 2

def parse_wider_warehouse(warehouse_str):
    warehouse = [list(line) for line in warehouse_str.strip().split('\n')]
    robot_pos = None
    boxes = []

    scaled = []
    for r, row in enumerate(warehouse):
        scaled.append([])
        for c, char in enumerate(row):
            if char == '@':
                robot_pos = (r, 2*c)
                scaled[r].append('.')
                scaled[r].append('.')
            elif char == 'O':
                boxes.append([(r, 2*c), (r, 2*c+1)])
                scaled[r].append('.')
                scaled[r].append('.')
            elif char == '#':
                scaled[r].append('#')
                scaled[r].append('#')
            elif char == '.':
                scaled[r].append('.')
                scaled[r].append('.')                

    return scaled, robot_pos, boxes

def display_wider_warehouse(warehouse, robot_pos, boxes):
    display = [row[:] for row in warehouse]
    #print(display)
    r, c = robot_pos
    display[r][c] = '@'
    for [(br1, bc1), (br2, bc2)] in boxes:
        display[br1][bc1] = '['
        display[br2][bc2] = ']'
    for row in display:
        print(''.join(row))

def move_robot_wider(warehouse, robot_pos, boxes, moves):
    directions = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}

    #display_wider_warehouse(warehouse, robot_pos, boxes)

    for move in moves:
        #print('=====================================')
        dr, dc = directions[move]
        #print('direction', dr, dc)
        nr, nc = robot_pos[0] + dr, robot_pos[1] + dc

        if warehouse[nr][nc] == '#':
            #print('wall ', nr, nc)
            #display_wider_warehouse(warehouse, robot_pos, boxes)
            continue

        cascade_path = []
        to_move = []
        can_move = True
        for box in boxes:
            # if new pos is a part of a box
            if (nr, nc) in box:
                #print('box ', box)
                
                # get each poart of the box
                br1, bc1 = box[0]
                br2, bc2 = box[1]
                
                # and get there updated possible possible
                nbr1, nbc1 = br1 + dr, bc1 + dc
                nbr2, nbc2 = br2 + dr, bc2 + dc

                # Check if the wide box can move
                if warehouse[nbr1][nbc1] == '#':
                    #print('Wall', nbr1,nbc1)
                    can_move = False
                    cascade_path = []
                    break

                if warehouse[nbr2][nbc2] == '#':
                    #print('Wall', nbr2,nbc2)
                    can_move = False
                    cascade_path = []
                    break

                # add those to be checked
                cascade_path.append((nbr1,nbc1))
                cascade_path.append((nbr2,nbc2))

                # this box is maybe to move
                to_move.append(box)

                while cascade_path:

                    cr,cc = cascade_path.pop()
                    #print(cr)
                    #print(cc)

                    # if part of a box is moving to a wall, not good
                    if warehouse[cr][cc] == '#':
                        cascade_path = []
                        to_move = []
                        can_move = False
                        break

                    # check if part of a box moves to another part of another box
                    for box2 in boxes:
                        if box2 in to_move:
                            #print('skip')
                            continue
                        if (cr,cc) in box2:
                            #print('also a box', cr, cc)
                            # if so, add two parts of this new box while moved to be check
                            bbr1, bbc1 = box2[0]
                            bbr2, bbc2 = box2[1]
                            
                            nnbr1, nnbc1 = bbr1 + dr, bbc1 + dc
                            nnbr2, nnbc2 = bbr2 + dr, bbc2 + dc

                            to_move.append(box2)

                            cascade_path.append((nnbr1,nnbc1))
                            cascade_path.append((nnbr2,nnbc2))                            

        if can_move:
            robot_pos = (nr, nc)
            for box in to_move:
                boxes.remove(box)
            for box in to_move:
                br1, bc1 = box[0]
                br2, bc2 = box[1]
                boxes.append([(br1+dr, bc1+dc), (br2+dr, bc2+dc)])

        #display_wider_warehouse(warehouse, robot_pos, boxes)

    return robot_pos, boxes

warehouse, robot_pos, boxes = parse_wider_warehouse(warehouse_str)
#print(warehouse)
#print(robot_pos)
#print(boxes)
#display_wider_warehouse(warehouse, robot_pos, boxes)
robot_pos, boxes = move_robot_wider(warehouse, robot_pos, boxes, moves)

def calculate_gps_sum_wider(boxes):
    return sum(100 * r + c for [(r, c),(_,__)] in boxes)

gps_sum = calculate_gps_sum_wider(boxes)
print('Sum of GPS coordinates:', gps_sum)