from urllib import request
from dotenv import load_dotenv
from collections import Counter
import os
load_dotenv()

url = 'https://adventofcode.com/2023/day/8/input'
token = os.getenv('aoc_token')

req = request.Request(
    url, headers={'Cookie': f'session={token}'})


def get_data():
    with request.urlopen(req) as f:
        lines = f.readlines()
        directions = lines[0].decode('utf-8').strip()
        lines.pop(0)

        data = {}
        for line in lines[1:]:
            if line.decode('utf-8').strip():
                key, value = line.decode('utf-8').strip().split(' = ')
                data[key] = tuple(value.strip('()').split(', '))
    return directions, data


def get_test_data():
    test_input = open('day8/input.txt', 'r').readlines()
    test_input = [line.strip() for line in test_input]

    directions = test_input[0]
    test_input.pop(0)

    data = {}

    for line in test_input[1:]:
        if line:
            key, value = line.split(' = ')
            data[key] = tuple(value.strip('()').split(', '))
    return directions, data


def traverse_directions(starting_point, directions, data):
    steps = 0
    current_point = starting_point

    while current_point != 'ZZZ':
        for direction in directions:
            steps += 1
            if direction == 'L':
                current_point = data[current_point][0]
            elif direction == 'R':
                current_point = data[current_point][1]
            else:
                raise Exception('Invalid direction')
            if current_point == 'ZZZ':
                break
        if current_point != 'ZZZ':
            continue
        else:
            break
    return steps


def traverse_route(starting_point, directions, data):
    steps = 0
    current_point = starting_point

    while current_point[-1] != 'Z':
        for direction in directions:
            if direction == 'L':
                current_point = data[current_point][0]

            elif direction == 'R':
                current_point = data[current_point][1]
            else:
                raise Exception('Invalid direction')
            steps += 1

            if current_point[-1] == 'Z':
                break
        if current_point[-1] != 'Z':
            continue
        else:
            break
    return steps


def traverse_as_ghost():
    directions, data = get_data()

    starting_points = [point for point in data if point[-1] == 'A']
    current_points = starting_points.copy()
    steps = 0

    while not all(point[-1] == 'Z' for point in current_points):
        for direction in directions:
            steps += 1
            for i, point in enumerate(current_points):
                if direction == 'L':
                    current_points[i] = data[point][0]
                elif direction == 'R':
                    current_points[i] = data[point][1]
                else:
                    raise Exception('Invalid direction')

            if all(point[-1] == 'Z' for point in current_points):
                return steps


directions, data = get_data()

print(f"Part 1: {traverse_directions('AAA', directions, data)}")
print(f"Part 2: {traverse_as_ghost()}")
