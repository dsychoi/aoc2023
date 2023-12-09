from urllib import request
import os
from dotenv import load_dotenv
load_dotenv()

url = 'https://adventofcode.com/2023/day/9/input'
token = os.getenv('aoc_token')

req = request.Request(
    url, headers={'Cookie': f'session={token}'})


def get_data():
    with request.urlopen(req) as f:
        lines = f.readlines()

        data = []
        for line in lines:
            if line.decode('utf-8').strip():
                new_line = line.decode('utf-8').strip().split(' ')
                new_line = [int(num) for num in new_line]
                data.append(new_line)
    return data

def get_predicted_appendage(sequence):
    new_sequence = sequence.copy()
    differences = [new_sequence]

    while not all(x == 0 for x in differences[-1]):
        differences.append([j - i for i, j in zip(differences[-1][:-1], differences[-1][1:])])

    for diff in reversed(differences[1:]):
        new_sequence.append(new_sequence[-1] + diff[-1])

    return new_sequence[-1]

def get_predicted_prependage(sequence):
    new_sequence = sequence.copy()
    new_sequence.reverse()
    differences = [new_sequence]
    last_elements = []

    while not all(x == 0 for x in differences[-1]):
        differences.append([j - i for i, j in zip(differences[-1][:-1], differences[-1][1:])])
        last_elements.append(differences[-1][-1])

    for last_element in reversed(last_elements):
        new_sequence.append(new_sequence[-1] + last_element)

    new_sequence.reverse()
    return new_sequence[0]
    
def appendage():
    # dataset = [[0, 3, 6, 9, 12, 15], [1, 3, 6, 10, 15, 21], [10, 13, 16, 21, 30, 45]]
    dataset = get_data()
    total = 0
    for sequence in dataset:
        total += get_predicted_appendage(sequence)
    return total

def prependage():
    # dataset = [[0, 3, 6, 9, 12, 15], [1, 3, 6, 10, 15, 21], [10, 13, 16, 21, 30, 45]]
    dataset = get_data()
    total = 0
    for sequence in dataset:
        total += get_predicted_prependage(sequence)
    return total

print(f"Part 1: {appendage()}")
print(f"Part 2: {prependage()}")