from urllib import request
import os
from dotenv import load_dotenv
load_dotenv()

url = 'https://adventofcode.com/2023/day/14/input'
token = os.getenv('aoc_token')

req = request.Request(
url, headers={'Cookie': f'session={token}'})


def get_data():
    with request.urlopen(req) as f:
        lines = f.readlines()

    data = []
    for line in lines:
        if line.decode('utf-8').strip():
            data.append(line.decode('utf-8').strip())            
    return data


test_input = open('day14/input.txt', 'r').readlines()
test_input = [line.strip() for line in test_input]


def tilt_north(platform):
    rows, cols = len(platform), len(platform[0])
    new_platform = [['.' for _ in range(cols)] for _ in range(rows)]

    for j in range(cols):
        insert_position = 0
        for i in range(rows):
            if platform[i][j] == '#':
                new_platform[i][j] = '#'
                insert_position = max(insert_position, i + 1)
            elif platform[i][j] == 'O':
                new_platform[insert_position][j] = 'O'
                insert_position += 1

    return new_platform

def calculate_load(platform):
    rows = len(platform)
    total_load = 0
    for i in range(rows):
        total_load += platform[i].count('O') * (rows - i)
    return total_load

platform = [
    list('O....#....'),
    list('O.OO#....#'),
    list('.....##...'),
    list('OO.#O....O'),
    list('.O.....O#.'),
    list('O.#..O.#.#'),
    list('..O..#O..O'),
    list('.......O..'),
    list('#....###..'),
    list('#OO..#....')
]

def tilt_south(platform):
    rows, cols = len(platform), len(platform[0])
    new_platform = [['.' for _ in range(cols)] for _ in range(rows)]

    for j in range(cols):
        insert_position = rows - 1
        for i in reversed(range(rows)):
            if platform[i][j] == '#':
                new_platform[i][j] = '#'
                insert_position = min(insert_position, i - 1)
            elif platform[i][j] == 'O':
                new_platform[insert_position][j] = 'O'
                insert_position -= 1

    return new_platform

def tilt_east(platform):
    rows, cols = len(platform), len(platform[0])
    new_platform = [['.' for _ in range(cols)] for _ in range(rows)]

    for i in range(rows):
        insert_position = cols - 1
        for j in reversed(range(cols)):
            if platform[i][j] == '#':
                new_platform[i][j] = '#'
                insert_position = min(insert_position, j - 1)
            elif platform[i][j] == 'O':
                new_platform[i][insert_position] = 'O'
                insert_position -= 1

    return new_platform

def tilt_west(platform):
    rows, cols = len(platform), len(platform[0])
    new_platform = [['.' for _ in range(cols)] for _ in range(rows)]

    for i in range(rows):
        insert_position = 0
        for j in range(cols):
            if platform[i][j] == '#':
                new_platform[i][j] = '#'
                insert_position = max(insert_position, j + 1)
            elif platform[i][j] == 'O':
                new_platform[i][insert_position] = 'O'
                insert_position += 1

    return new_platform


def run_cycles(platform, cycles):
    states = []
    for cycle in range(cycles):
        for tilt in [tilt_north, tilt_west, tilt_south, tilt_east]:
            platform = tilt(platform)
        if platform in states:
            index = states.index(platform)
            cycle_length = len(states) - index
            remaining_cycles = (cycles - cycle) % cycle_length
            if remaining_cycles == 0:
                return calculate_load(states[index])
            else:
                return calculate_load(states[index + remaining_cycles - 1])
        states.append(platform)
    return calculate_load(platform)


print(run_cycles(get_data(), 1000000000))