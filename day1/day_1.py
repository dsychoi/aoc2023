from urllib import request
import os
from dotenv import load_dotenv
load_dotenv()

# input = open('day1/input.txt', 'r').readlines()

url = 'https://adventofcode.com/2023/day/1/input'
token = os.getenv('aoc_token')

req = request.Request(
    url, headers={'Cookie': f'session={token}'})


def get_calibration_value():
    sum = 0

    with request.urlopen(req) as f:
        for line in f.readlines():
            line = line.decode('utf-8').strip()
            current_line_number = ''
            for i in range(len(line)):
                if line[i].isdigit():
                    current_line_number += line[i]
                    break
            for i in range(len(line) - 1, -1, -1):
                if line[i].isdigit():
                    current_line_number += line[i]
                    break
            sum += int(current_line_number)
    return sum


def get_true_calibration_value():
    sum = 0
    word_dict = {
        'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4',
        'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'
    }

    with request.urlopen(req) as f:
        for line in f.readlines():
            line = line.decode('utf-8').strip()
            new_line = line
            for word, number in word_dict.items():
                new_line = new_line.replace(word, word[0] + number + word[-1])

            current_line_number = ''
            for char in new_line:
                if char.isdigit():
                    current_line_number += char
                    break
            for char in reversed(new_line):
                if char.isdigit():
                    current_line_number += char
                    break

            sum += int(current_line_number)
        return sum


print(f'Calibration value: {get_calibration_value()}')
print(f'True calibration value: {get_true_calibration_value()}')
