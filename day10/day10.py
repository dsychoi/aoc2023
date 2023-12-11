from urllib import request
import os
from collections import deque
from dotenv import load_dotenv
load_dotenv()

url = 'https://adventofcode.com/2023/day/10/input'
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
    return data

test_input = open('day10/input.txt', 'r').readlines()
test_input = [line.strip() for line in test_input]

def parse_input(input_list):
    grid = { (r, c): value for r, row in enumerate(input_list) for c, value in enumerate(row)}
    start_position = next((position for position, value in grid.items() if value == 'S'), None)
    return grid, start_position

pipe_types = {
    '|': [('N', 'S')],
    '-': [('E', 'W')],
    'L': [('N', 'E')],
    'J': [('N', 'W')],
    '7': [('S', 'W')],
    'F': [('S', 'E')],
    'S': [('E', 'W')]
}

direction_offsets = {
    'N': (-1, 0),
    'S': (1, 0),
    'E': (0, 1),
    'W': (0, -1)
}

def add_edges(grid):
    adjacency_list = {position: [] for position in grid}

    for position, value in grid.items():
        if value in pipe_types:
            for direction_pair in pipe_types[value]:
                for direction in direction_pair:
                    offset = direction_offsets[direction]
                    neighbor_position = (position[0] + offset[0], position[1] + offset[1])
                    if neighbor_position in grid and grid[neighbor_position] != '.':
                        adjacency_list[position].append(neighbor_position)

    for position, neighbors in list(adjacency_list.items()):
        for neighbor in neighbors:
            if position not in adjacency_list[neighbor]:
                adjacency_list[position].remove(neighbor)

    return adjacency_list

def bfs_farthest_point(adjacency_list, start_position):
    visited = {position: False for position in adjacency_list}
    distance = {position: 0 for position in adjacency_list}
    queue = deque([start_position])

    visited[start_position] = True
    farthest_point = start_position
    max_distance = 0

    while queue:
        current_position = queue.popleft()
        for neighbor in adjacency_list[current_position]:
            if not visited[neighbor]:
                visited[neighbor] = True
                distance[neighbor] = distance[current_position] + 1
                queue.append(neighbor)
                if distance[neighbor] > max_distance:
                    farthest_point = neighbor
                    max_distance = distance[neighbor]

    return farthest_point, max_distance