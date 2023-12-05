from urllib import request
from collections import deque, defaultdict
from dotenv import load_dotenv
import os
import bisect
import heapq
import time
from intervaltree import Interval, IntervalTree
load_dotenv()

url = 'https://adventofcode.com/2023/day/5/input'
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


def parse_input(input_list):
    data_dict = {}
    current_key = None

    for line in input_list:
        if line:
            if ':' in line:
                current_key = line.split(':')[0].strip()
                values = list(map(int, line.split(':')[1].strip().split()))
                data_dict[current_key] = values if current_key == 'seeds' else []
            else:
                values = tuple(map(int, line.split()))
                data_dict[current_key].append(values)

    return data_dict


test_input = open('day5/input.txt', 'r').readlines()
test_input = [line.strip() for line in test_input]


def map_value(value, mapping):
    for destination, source, range in mapping:
        if source <= value < source + range:
            return destination + (value - source)
    return value


def solve(data):
    seeds = data['seeds']
    mappings = [
        data['seed-to-soil map'],
        data['soil-to-fertilizer map'],
        data['fertilizer-to-water map'],
        data['water-to-light map'],
        data['light-to-temperature map'],
        data['temperature-to-humidity map'],
        data['humidity-to-location map']
    ]

    min_location = float('inf')
    for seed in seeds:
        value = seed
        for mapping in mappings:
            value = map_value(value, mapping)
        min_location = min(min_location, value)

    return min_location


def map_range(start, length, mapping):
    tree = IntervalTree()
    for dest_start, src_start, range_length in mapping:
        tree[src_start:src_start+range_length] = dest_start
    intervals = sorted(tree[start:start+length])
    new_ranges = []
    prev_end = start
    for interval in intervals:
        if prev_end < interval.begin:
            new_ranges.append((prev_end, interval.begin - prev_end))
        overlap_start = max(prev_end, interval.begin)
        overlap_end = min(start + length, interval.end)
        new_start = interval.data + (overlap_start - interval.begin)
        new_end = interval.data + (overlap_end - interval.begin)
        new_ranges.append((new_start, new_end - new_start))
        prev_end = overlap_end
    if prev_end < start + length:
        new_ranges.append((prev_end, start + length - prev_end))
    return new_ranges


def lowest_location(data):
    t0 = time.time()
    seeds = data['seeds']
    seeds = [(seeds[i], seeds[i+1]) for i in range(0, len(seeds), 2)]
    mappings = [
        data['seed-to-soil map'],
        data['soil-to-fertilizer map'],
        data['fertilizer-to-water map'],
        data['water-to-light map'],
        data['light-to-temperature map'],
        data['temperature-to-humidity map'],
        data['humidity-to-location map']
    ]
    for mapping in mappings:
        new_seeds = []
        for start, length in seeds:
            new_seeds.extend(map_range(start, length, mapping))
        seeds = new_seeds
    t1 = time.time()
    print(f'Elapsed: {t1-t0} seconds')
    return min(start for start, length in seeds)


print(f'Part 1: {solve(parse_input(get_input()))}')
print(f'Part 2: {lowest_location(parse_input(get_input()))}')
