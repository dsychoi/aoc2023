from urllib import request
import os
from itertools import combinations
from collections import deque
from dotenv import load_dotenv
load_dotenv()

url = 'https://adventofcode.com/2023/day/11/input'
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
            # remove \n and b
            
    return data

test_input = open('day11/input.txt', 'r').readlines()
test_input = [line.strip() for line in test_input]

input = get_data()

def expand_universe(universe):
    expanded_rows = []
    for row in universe:
        if '#' not in row:
            expanded_rows.append(row)
            expanded_rows.append(row)
        else:
            expanded_rows.append(row)

    expanded_universe = []
    for row in zip(*expanded_rows):
        if '#' not in ''.join(row):
            expanded_universe.append(row)
            expanded_universe.append(row)
        else:
            expanded_universe.append(row)

    expanded_universe = [''.join(row) for row in zip(*expanded_universe)]
    return expanded_universe

def bfs(universe, start):
    queue = deque([start])
    distances = {start: 0}
    while queue:
        x, y = queue.popleft()
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(universe) and 0 <= ny < len(universe[0]) and (nx, ny) not in distances:
                distances[nx, ny] = distances[x, y] + 1
                queue.append((nx, ny))
    return distances

def solve(universe):
    universe = expand_universe(universe)
    galaxies = [(i, j) for i, row in enumerate(universe) for j, cell in enumerate(row) if cell == '#']
    distances = {galaxy: bfs(universe, galaxy) for galaxy in galaxies}
    total = 0
    for (x1, y1), (x2, y2) in combinations(galaxies, 2):
        total += distances[x1, y1][x2, y2]

    numbered_universe = [list(row) for row in universe]
    for i, (x, y) in enumerate(galaxies, 1):
        numbered_universe[x][y] = str(i)
    for row in numbered_universe:
        print(''.join(row))

    return total

def count_empty_spaces(universe):
    empty_rows = sum(1 for row in universe if '#' not in row)
    empty_cols = sum(1 for col in zip(*universe) if '#' not in col)
    return empty_rows, empty_cols

def bfs_2(universe, start, expansion_factor):
    queue = deque([start])
    distances = {start: 0}
    while queue:
        x, y = queue.popleft()
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(universe) and 0 <= ny < len(universe[0]) and (nx, ny) not in distances:
                # Determine if the next step is through an empty row or column
                through_empty_space = (dx != 0 and '#' not in universe[nx]) or (dy != 0 and '#' not in [row[ny] for row in universe])
                step_distance = expansion_factor if through_empty_space else 1
                distances[nx, ny] = distances[x, y] + step_distance
                queue.append((nx, ny))
    return distances

def solve_2(universe):
    expansion_factor = 1000000
    galaxies = [(i, j) for i, row in enumerate(universe) for j, cell in enumerate(row) if cell == '#']
    distances = {galaxy: bfs_2(universe, galaxy, expansion_factor) for galaxy in galaxies}
    total = 0
    for (x1, y1), (x2, y2) in combinations(galaxies, 2):
        total += distances[x1, y1][x2, y2]

    return total

print(solve_2(get_data()))
