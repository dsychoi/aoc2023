from urllib import request
import os
from dotenv import load_dotenv
import re
load_dotenv()

url = 'https://adventofcode.com/2023/day/2/input'
token = os.getenv('aoc_token')

req = request.Request(
    url, headers={'Cookie': f'session={token}'})


test_str = 'Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green'
# Convert into a dictionary with game # as key and list of 3-tuples as values representing RGB


def get_clean_line(line):
    return line.split(':')[1].split(';')


def get_rgb_triple(game_set):
    matches = re.findall(r'(\d+)\s*(\w+)', game_set)
    color_dict = {color: int(num) for num, color in matches}
    return (color_dict.get('red', 0), color_dict.get(
        'green', 0), color_dict.get('blue', 0))


def get_dict_item(game_number, game_sets):
    values = []
    for game_set in game_sets:
        values.append(get_rgb_triple(game_set))
    return {game_number: values}


def get_clean_data():
    games = {}

    with request.urlopen(req) as f:
        for index, line in enumerate(f.readlines()):
            line = line.decode('utf-8').strip()
            games.update(get_dict_item(index + 1, get_clean_line(line)))
    return games


def remove_invalid_games(games, r, g, b):
    keys = list(games.keys())
    for key in keys:
        for rgb in games[key]:
            if rgb[0] > r or rgb[1] > g or rgb[2] > b:
                del games[key]
                break
    return games


def get_minimum_needed(game_sets):
    max_red, max_green, max_blue = 0, 0, 0
    for game_set in game_sets:
        max_red = max(max_red, game_set[0])
        max_green = max(max_green, game_set[1])
        max_blue = max(max_blue, game_set[2])
    return (max_red, max_green, max_blue)


def get_sum_of_ids():
    games = get_clean_data()
    games = remove_invalid_games(games, 12, 13, 14)
    return sum(games.keys())


def power_of_tuple(rgb):
    return rgb[0] * rgb[1] * rgb[2]


def get_sum_of_set_powers():
    games = get_clean_data()
    sum = 0
    for game in games.values():
        sum += power_of_tuple(get_minimum_needed(game))
    return sum


print('Part 1: Sum of IDs =', get_sum_of_ids())
print('Part 2: Sum of set powers =', get_sum_of_set_powers())
