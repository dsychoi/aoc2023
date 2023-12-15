from urllib import request
import os
from dotenv import load_dotenv
load_dotenv()

url = 'https://adventofcode.com/2023/day/15/input'
token = os.getenv('aoc_token')

req = request.Request(
url, headers={'Cookie': f'session={token}'})


def get_data():
    with request.urlopen(req) as f:
        lines = f.readlines()

    data = []
    index = 0
    for line in lines:
        index += 1
        if line.decode('utf-8').strip():
            for string in line.decode('utf-8').strip().split(','):
                data.append(string)
    return data


def hash_code(string):
    result = 0
    for character in string:
        result += ord(character)
        result *= 17
        result = result % 256
    return result


def parsed_hash_code(string):
    if '=' in string:
        label, focal_length = string.split('=')
        lens = f"{label} {focal_length}"
    elif '-' in string:
        label, focal_length = string.split('-')[0], None
        lens = None
    else:
        raise ValueError("X")

    box = hash_code(label)
    return box, label, focal_length, lens

def focusing_power(box_number, lens_slot, focal_length):
    return (1 + box_number) * lens_slot * focal_length

puzzle_input = get_data()
test_input = ['rn=1', 'cm-', 'qp=3', 'cm=2' , 'qp-', 'pc=4', 'ot=9', 'ab=5', 'pc-', 'pc=6', 'ot=7']


def initialize_boxes():
    boxes = {i: [] for i in range(256)}

    for string in get_data():
        box, label, _, lens = parsed_hash_code(string)
        if lens is None:
            for box_lens in boxes[box]:
                if box_lens.startswith(label):
                    boxes[box].remove(box_lens)
        else:
            replaced = False
            for box_lens in boxes[box]:
                if box_lens.startswith(label):
                    index = next(i for i, item in enumerate(boxes[box]) if item.startswith(label))
                    boxes[box][index] = lens
                    replaced = True
            if not replaced:
                boxes[box].append(lens)
    return boxes

def solve():
    boxes = initialize_boxes()
    total_focusing_power = 0

    for key, value in boxes.items():
        for index, item in enumerate(value):
            total_focusing_power += (focusing_power(key, index + 1, int(item[-1])))

    return total_focusing_power

print(solve())