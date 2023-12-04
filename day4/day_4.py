from urllib import request
from collections import deque
from dotenv import load_dotenv
import os
import re
load_dotenv()

url = 'https://adventofcode.com/2023/day/4/input'
token = os.getenv('aoc_token')

req = request.Request(
    url, headers={'Cookie': f'session={token}'})


def get_input():
    input = []

    with request.urlopen(req) as f:
        for line in f.readlines():
            line = line.decode('utf-8').strip()
            input.append(line)
    return input


def parse_card(card):
    card = card.split(':')[1].split('|')
    winning_numbers = card[0].split()
    card_numbers = card[1].split()
    winning_set = set(winning_numbers)
    card_set = set(card_numbers)
    return winning_set, card_set


def get_total_points():
    input = get_input()
    total = 0
    for index, line in enumerate(input):
        card_total = 0
        winning_set, card_set = parse_card(line)
        matches = winning_set.intersection(card_set)
        for index in range(len(matches)):
            if index == 0:
                card_total += 1
            else:
                card_total *= 2
        total += card_total
    return total


test_game = open('day4/input.txt', 'r').readlines()
test_game = [line.strip() for line in test_game]


def get_total_scratchcards():
    input = get_input()
    total_cards = len(input)
    matches = [0] * total_cards
    total_scratchcards = 0

    for index in range(total_cards):
        line = input[index]
        winning_set, card_set = parse_card(line)
        matches[index] = len(winning_set.intersection(card_set))

    cards_to_process = deque(range(total_cards))
    while cards_to_process:
        index = cards_to_process.popleft()
        total_scratchcards += 1
        for i in range(1, matches[index] + 1):
            next_card_index = index + i
            if next_card_index < total_cards:
                cards_to_process.append(next_card_index)

    return total_scratchcards


print('Part 1:', get_total_points())
print('Part 2:', get_total_scratchcards())
