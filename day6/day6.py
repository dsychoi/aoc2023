
races_test = [(7, 9), (15, 40), (30, 200)]
races = [(61, 643), (70, 1184), (90, 1362), (66, 1041)]
races_2 = [(61709066, 643118413621041)]


def get_number_of_ways_to_win(race):
    res = 0
    for i in range(race[0]):
        elapsed_time = speed = i + 1
        remaining_time = race[0] - elapsed_time
        distance_traveled = speed * remaining_time
        if distance_traveled > race[1]:
            res += 1
    print(res)
    return res


def solve(races):
    ans = 1
    for race in races:
        ans *= get_number_of_ways_to_win(race)
    return ans


print(f'Part 1: {solve(races)}')
print(f'Part 2: {solve(races_2)}')
