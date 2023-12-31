from urllib import request
from dotenv import load_dotenv
from collections import Counter
import os
load_dotenv()

url = 'https://adventofcode.com/2023/day/7/input'
token = os.getenv('aoc_token')

req = request.Request(
    url, headers={'Cookie': f'session={token}'})


def get_input():
    input = []

    with request.urlopen(req) as f:
        for line in f.readlines():
            line = line.decode('utf-8').strip()
            line = line.split(' ')
            input.append([line[0], line[1]])
    return input


test_input = open('day5/input.txt', 'r').readlines()
test_input = [line.strip() for line in test_input]


card_values = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10,
               '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}


def get_strength(hand):
    hand_values = [card_values[card] for card in hand]
    print(hand_values)


def get_new_input():
    input = get_input()
    for line in input:
        strengths = dict(Counter(line[0]))
        twos_count = sum(1 for value in strengths.values() if value == 2)

        if 5 in strengths.values():
            line.append(7)
        elif 4 in strengths.values():
            line.append(6)
        elif 3 in strengths.values() and 2 in strengths.values():
            line.append(5)
        elif 3 in strengths.values():
            line.append(4)
        elif 2 in strengths.values():
            if twos_count > 1:
                line.append(3)
            else:
                line.append(2)
        else:
            line.append(1)
        line.append([card_values[card] for card in line[0]])
    input.sort(key=lambda x: (-x[2], [-i for i in x[3]]), reverse=True)

    return input


card_values_joker = {'A': 13, 'K': 12, 'Q': 11, 'T': 10,
                     '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2, 'J': 1}


def solve():
    input = get_new_input()
    winnings = 0
    for index, line in enumerate(input):
        # print(index + 1, line[2], line[0], line[3])
        winnings += (index + 1) * int(line[1])
    return winnings


def get_new_input_joker():
    input = get_input()
    for line in input:
        strengths = dict(Counter(line[0]))
        twos_count = sum(1 for value in strengths.values() if value == 2)
        joker_count = strengths.get('J', 0)
        
        # Exclude 'J' from the strengths dictionary before calculating highest_count
        if 'J' in strengths:
            del strengths['J']
        highest_count = max(strengths.values(), default=0)

        if (highest_count + joker_count) >= 5:  # 5 of a kind
            line.append(7)
        elif (highest_count + joker_count) == 4:  # 4 of a kind
            line.append(6)
        elif (3 in strengths.values() and 2 in strengths.values()) or (twos_count == 2 and joker_count == 1):  # full house
            line.append(5)
        elif (highest_count + joker_count) == 3:  # 3 of a kind
            line.append(4)
        elif (twos_count == 2) or (twos_count == 1 and joker_count == 1):  # 2 pairs
            line.append(3)
        elif (twos_count == 1) or (joker_count == 1):  # 1 pair
            line.append(2)
        else:  # high card
            line.append(1)
        line.append([card_values_joker[card] for card in line[0]])
    input.sort(key=lambda x: (-x[2], [-i for i in x[3]]), reverse=True)

    return input


def solve_joker():
    input = get_new_input_joker()
    winnings = 0
    for index, line in enumerate(input):
        print(index + 1, line[2], line[0], line[3])
        winnings += (index + 1) * int(line[1])
    return winnings


print(f'Part 1: ${solve()}')
print(f'Part 2: ${solve_joker()}')
