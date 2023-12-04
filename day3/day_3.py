from urllib import request
from dotenv import load_dotenv
import os
import re
load_dotenv()

url = 'https://adventofcode.com/2023/day/3/input'
token = os.getenv('aoc_token')

req = request.Request(
    url, headers={'Cookie': f'session={token}'})


def get_schematic():
    schematic = []

    with request.urlopen(req) as f:
        for index, line in enumerate(f.readlines()):
            line = line.decode('utf-8').strip()
            schematic.append([char for char in line])
    return schematic


# def sum_of_part_numbers(schematic):
#     valid_symbols = "!@#$%^&*()_-+={}[]"

#     for i, row in enumerate(schematic):
#         left = 0
#         right = 0
#         for j, column in enumerate(row):
#             if column.isdigit():
#                 left = j
#                 break


def sum_part_numbers(schematic):
    symbols = {'@', '#', '*', '%', '&', '-', '+',
               '=', '{', '}', '[', ']', '$', '/'}
    total = 0
    rows, cols = len(schematic), len(schematic[0])

    def get_number(i, j):
        number = ''
        while j < cols and schematic[i][j].isdigit():
            number += schematic[i][j]
            j += 1
        return int(number) if number else None, j

    def is_adjacent_to_symbol(i, j):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = i + dx, j + dy
                if 0 <= nx < rows and 0 <= ny < cols and schematic[nx][ny] in symbols:
                    return True
        return False

    for i in range(rows):
        j = 0
        while j < cols:
            if schematic[i][j].isdigit():
                number, end = get_number(i, j)
                if any(is_adjacent_to_symbol(i, k) for k in range(j, end)):
                    total += number
                j = end
            else:
                j += 1
    return total


def sum_gear_ratios(schematic):
    symbols = {'*'}
    total = 0
    rows, cols = len(schematic), len(schematic[0])
    pairs = []

    def get_number(i, j):
        number = ''
        while j < cols and schematic[i][j].isdigit():
            number += schematic[i][j]
            j += 1
        return int(number) if number else None, j

    def get_adjacent_numbers(i, j):
        numbers = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = i + dx, j + dy
                if 0 <= nx < rows and 0 <= ny < cols and schematic[nx][ny].isdigit():
                    while ny > 0 and schematic[nx][ny-1].isdigit():
                        ny -= 1
                    number, _ = get_number(nx, ny)
                    if number is not None and number not in numbers:
                        numbers.append(number)
        return numbers

    for i in range(rows):
        for j in range(cols):
            if schematic[i][j] in symbols:
                numbers = get_adjacent_numbers(i, j)
                if len(numbers) >= 2:
                    pairs.append(tuple(numbers[:2]))

    for pair in pairs:
        print(pair)
        total += pair[0] * pair[1]

    return total


test_schematic = open('day3/input.txt', 'r').readlines()
test_schematic = [line.strip() for line in test_schematic]


print('Part 1: Sum of part numbers =', sum_part_numbers(get_schematic()))
print('Part 2: Sum of gear ratios =', sum_gear_ratios(get_schematic()))
