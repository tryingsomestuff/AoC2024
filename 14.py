def parse(data):
    robots = []
    for line in data:
        position, velocity = line.split(' v=')
        px, py = map(int, position[2:].split(','))
        vx, vy = map(int, velocity.split(','))
        robots.append(((px, py), (vx, vy)))
    return robots

def update_position(pos, vel, width, height):
    x, y = pos
    vx, vy = vel
    x = (x + vx) % width
    y = (y + vy) % height
    return x, y

def simulate_robots(robots, width, height, time_steps):
    for _ in range(time_steps):
        robots = [(update_position(pos, vel, width, height), vel) for pos, vel in robots]
    return robots

def count_quadrants(robots, width, height):
    mid_x, mid_y = width // 2, height // 2
    quadrants = [0, 0, 0, 0]

    for (x, y), _ in robots:
        if x == mid_x or y == mid_y:
            continue
        if x < mid_x and y < mid_y:
            quadrants[0] += 1
        elif x >= mid_x and y < mid_y:
            quadrants[1] += 1
        elif x < mid_x and y >= mid_y:
            quadrants[2] += 1
        else:
            quadrants[3] += 1

    return quadrants

def calculate_safety_factor(quadrants):
    safety_factor = 1
    for count in quadrants:
        safety_factor *= count
    return safety_factor

def read(fn):
    with open(fn, 'r') as file:
        lines = file.read().strip().split('\n')
    return lines

# Sample
input_data = '''
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
'''

width = 11
height = 7
time_steps = 100

robots = parse(input_data.strip().split('\n'))
robots_after_simulation = simulate_robots(robots, width, height, time_steps)
quadrant_counts = count_quadrants(robots_after_simulation, width, height)
safety_factor = calculate_safety_factor(quadrant_counts)
print('Quadrant counts:', quadrant_counts)
print('Safety factor:', safety_factor)

# Real
input_data = read('data/data14')

width = 11
height = 7

width = 101
height = 103

time_steps = 100

robots = parse(input_data)
robots_after_simulation = simulate_robots(robots, width, height, time_steps)
quadrant_counts = count_quadrants(robots_after_simulation, width, height)
safety_factor = calculate_safety_factor(quadrant_counts)
print('Quadrant counts:', quadrant_counts)
print('Safety factor:', safety_factor)


# Part 2
# Generate all image and have a look at them ... (7709)
from PIL import Image, ImageDraw
import os
if not os.path.exists('output/14/'):
    os.makedirs('output/14/')


def create_robot_image(robots, width, height, filename):
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    for pos, _ in robots:
        x, y = pos
        draw.point((x, y), fill='black')
    img.save(filename)

all = []
for t in range(1,100000):
    robots = [(update_position(pos, vel, width, height), vel) for pos, vel in robots]
    if t == 7709:
        create_robot_image(robots, width, height, f'output/14/robots_{t}.png')
    if robots in all:
        print('repeat ', t)
        break
    all.append(robots)