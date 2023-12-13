from urllib import request
import os
from itertools import combinations
from collections import deque
from dotenv import load_dotenv
load_dotenv()

url = 'https://adventofcode.com/2023/day/13/input'
token = os.getenv('aoc_token')

req = request.Request(
url, headers={'Cookie': f'session={token}'})


def get_data():
    with request.urlopen(req) as f:
        lines = f.readlines()

    patterns = []
    pattern = []
    for line in lines:
        if line.decode('utf-8').strip():
            pattern.append(line.decode('utf-8').strip())
        else:
            patterns.append(pattern)
            pattern = []
    if pattern:
        patterns.append(pattern)
    return patterns


test_input = open('day11/input.txt', 'r').readlines()
test_input = [line.strip() for line in test_input]

# Example pattern
pattern = [
    # '.##.###..#.......',
    # '..##.#..#...#..#.',
    # '####.......##..##',
    # '.##......#.##..##',
    # '..#.####.........',
    # '..#.####.........',
    # '###......#.##..##',
    # '####.......##..##',
    # '..##.#..#...#..#.',
    # '.##.###..#.......',
    # '...##...#....##..',
    # '#.##.#...####..##',
    # '##..#.##..#.#..#.',
    # '...#####..#.####.',
    # '..##..#.##.......',
    # '##.######..#.##.#',
    # '.##.##...##......'
    '#...##..#',
    '#....#..#',
    '..##..###',
    '#####.##.',
    '#####.##.',
    '..##..###',
    '#....#..#'
]

patterns = [
    [
    '#...##..#',
    '#....#..#',
    '..##..###',
    '#####.##.',
    '#####.##.',
    '..##..###',
    '#....#..#'
    ],
    [
    '#.##..##.',
    '..#.##.#.',
    '##......#',
    '##......#',
    '..#.##.#.',
    '..##..##.',
    '#.#.##.#.'
    ]
]


def get_reflection_number(rows):
    columns = [list(column) for column in zip(*rows)]

    for i in range(len(columns)):
        if i <= len(columns) // 2:
            mirrored_range = columns[-(i * 2):]
            if mirrored_range == mirrored_range[::-1]:
                return len(columns) - i
        else:
            mirrored_range = columns[:-(len(columns) - ((len(columns) - i) * 2))]
            if mirrored_range == mirrored_range[::-1]:
                return len(columns) - i


    for i in range(len(rows)):
        if i <= len(rows) // 2:
            mirrored_range = rows[-(i * 2):]
            if mirrored_range == mirrored_range[::-1]:
                return (len(rows) - i) * 100
        else:
            mirrored_range = rows[:-(len(rows) - ((len(rows) - i) * 2))]
            if mirrored_range == mirrored_range[::-1]:
                return (len(rows) - i) * 100

    return 0

def count_mismatches(s1, s2):
    if len(s1) != len(s2):
        raise ValueError("Both strings must be of equal length")
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

# Find reflection index
reflection_index = get_reflection_number(pattern)

def solve():
    total = 0
    patterns = get_data()
    for pattern in patterns:
        total += get_reflection_number(pattern)
    return total

def smudge_solve():
    total = 0
    # patterns = get_data()
    # for pattern in patterns:
        # total += get_smudged_reflection_number(pattern)
    return total


print(f"Part 1: {solve()}")
print(f"Part 2: {smudge_solve()}")

