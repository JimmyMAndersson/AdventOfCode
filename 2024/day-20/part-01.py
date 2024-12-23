import os
import numpy as np
from functools import cache
from itertools import combinations

# --- Day 20: Race Condition ---
# The Historians are quite pixelated again. This time, a massive, black building looms over you - you're right outside the CPU!
#
# While The Historians get to work, a nearby program sees that you're idle and challenges you to a race. Apparently, you've arrived just in time for the frequently-held race condition festival!
#
# The race takes place on a particularly long and twisting code path; programs compete to see who can finish in the fewest picoseconds. The winner even gets their very own mutex!
#
# They hand you a map of the racetrack (your puzzle input). For example:
#
# ###############
# #...#...#.....#
# #.#.#.#.#.###.#
# #S#...#.#.#...#
# #######.#.#.###
# #######.#.#...#
# #######.#.###.#
# ###..E#...#...#
# ###.#######.###
# #...###...#...#
# #.#####.#.###.#
# #.#...#.#.#...#
# #.#.#.#.#.#.###
# #...#...#...###
# ###############
# The map consists of track (.) - including the start (S) and end (E) positions (both of which also count as track) - and walls (#).
#
# When a program runs through the racetrack, it starts at the start position. Then, it is allowed to move up, down, left, or right; each such move takes 1 picosecond. The goal is to reach the end position as quickly as possible. In this example racetrack, the fastest time is 84 picoseconds.
#
# Because there is only a single path from the start to the end and the programs all go the same speed, the races used to be pretty boring. To make things more interesting, they introduced a new rule to the races: programs are allowed to cheat.
#
# The rules for cheating are very strict. Exactly once during a race, a program may disable collision for up to 2 picoseconds. This allows the program to pass through walls as if they were regular track. At the end of the cheat, the program must be back on normal track again; otherwise, it will receive a segmentation fault and get disqualified.
#
# So, a program could complete the course in 72 picoseconds (saving 12 picoseconds) by cheating for the two moves marked 1 and 2:
#
# ###############
# #...#...12....#
# #.#.#.#.#.###.#
# #S#...#.#.#...#
# #######.#.#.###
# #######.#.#...#
# #######.#.###.#
# ###..E#...#...#
# ###.#######.###
# #...###...#...#
# #.#####.#.###.#
# #.#...#.#.#...#
# #.#.#.#.#.#.###
# #...#...#...###
# ###############
# Or, a program could complete the course in 64 picoseconds (saving 20 picoseconds) by cheating for the two moves marked 1 and 2:
#
# ###############
# #...#...#.....#
# #.#.#.#.#.###.#
# #S#...#.#.#...#
# #######.#.#.###
# #######.#.#...#
# #######.#.###.#
# ###..E#...12..#
# ###.#######.###
# #...###...#...#
# #.#####.#.###.#
# #.#...#.#.#...#
# #.#.#.#.#.#.###
# #...#...#...###
# ###############
# This cheat saves 38 picoseconds:
#
# ###############
# #...#...#.....#
# #.#.#.#.#.###.#
# #S#...#.#.#...#
# #######.#.#.###
# #######.#.#...#
# #######.#.###.#
# ###..E#...#...#
# ###.####1##.###
# #...###.2.#...#
# #.#####.#.###.#
# #.#...#.#.#...#
# #.#.#.#.#.#.###
# #...#...#...###
# ###############
# This cheat saves 64 picoseconds and takes the program directly to the end:
#
# ###############
# #...#...#.....#
# #.#.#.#.#.###.#
# #S#...#.#.#...#
# #######.#.#.###
# #######.#.#...#
# #######.#.###.#
# ###..21...#...#
# ###.#######.###
# #...###...#...#
# #.#####.#.###.#
# #.#...#.#.#...#
# #.#.#.#.#.#.###
# #...#...#...###
# ###############
# Each cheat has a distinct start position (the position where the cheat is activated, just before the first move that is allowed to go through walls) and end position; cheats are uniquely identified by their start position and end position.
#
# In this example, the total number of cheats (grouped by the amount of time they save) are as follows:
#
# There are 14 cheats that save 2 picoseconds.
# There are 14 cheats that save 4 picoseconds.
# There are 2 cheats that save 6 picoseconds.
# There are 4 cheats that save 8 picoseconds.
# There are 2 cheats that save 10 picoseconds.
# There are 3 cheats that save 12 picoseconds.
# There is one cheat that saves 20 picoseconds.
# There is one cheat that saves 36 picoseconds.
# There is one cheat that saves 38 picoseconds.
# There is one cheat that saves 40 picoseconds.
# There is one cheat that saves 64 picoseconds.
# You aren't sure what the conditions of the racetrack will be like, so to give yourself as many options as possible, you'll need a list of the best cheats. How many cheats would save you at least 100 picoseconds?

@cache
def get_next_positions(position):
    x, y = position

    return set([
        (x - 1, y),
        (x + 1, y),
        (x, y - 1),
        (x, y + 1)
    ])

def find_path(start, track, end):
    queue = [start]
    visited = set()
    
    while len(queue) > 0:
        path = queue.pop()

        if path[-1] == end:
            return path

        visited.add(path[-1])
        next_positions = (get_next_positions(path[-1]) - track) - visited

        for next_position in next_positions:
            queue.append(path + (next_position,))
        
    return None

def find_cheats(path):
    cheats = {}
    for ((lhs_time, lhs_location), (rhs_time, rhs_location)) in combinations(enumerate(path), 2):
        if rhs_time - lhs_time <= 2:
            continue

        manhattan_distance = abs(lhs_location[0] - rhs_location[0]) + abs(lhs_location[1] - rhs_location[1])
        
        if manhattan_distance <= 2:
            cheats[(lhs_location, rhs_location)] = rhs_time - lhs_time - manhattan_distance
    
    return cheats

if __name__ == '__main__':
    file_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(file_path)
    input_path = os.path.join(dir_path, 'input')
    
    with open(input_path, 'r') as file:
        data = [line.strip() for line in file.readlines()]
        data = np.array(data, dtype=str)
        data = data.view('U1').reshape(data.size, -1)

        track = set(zip(*np.where(data == '#')))
        start = tuple(zip(*np.where(data == 'S')))[0]
        end = tuple(zip(*np.where(data == 'E')))[0]

        path = find_path((start,), track, end)
        cheats = { k: v for k, v in find_cheats(path).items() if v >= 100 }

        print(len(cheats))
