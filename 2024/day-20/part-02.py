import os
import numpy as np
from functools import cache
from itertools import combinations

# --- Part Two ---
# The programs seem perplexed by your list of cheats. Apparently, the two-picosecond cheating rule was deprecated several milliseconds ago! The latest version of the cheating rule permits a single cheat that instead lasts at most 20 picoseconds.
#
# Now, in addition to all the cheats that were possible in just two picoseconds, many more cheats are possible. This six-picosecond cheat saves 76 picoseconds:
#
# ###############
# #...#...#.....#
# #.#.#.#.#.###.#
# #S#...#.#.#...#
# #1#####.#.#.###
# #2#####.#.#...#
# #3#####.#.###.#
# #456.E#...#...#
# ###.#######.###
# #...###...#...#
# #.#####.#.###.#
# #.#...#.#.#...#
# #.#.#.#.#.#.###
# #...#...#...###
# ###############
# Because this cheat has the same start and end positions as the one above, it's the same cheat, even though the path taken during the cheat is different:
#
# ###############
# #...#...#.....#
# #.#.#.#.#.###.#
# #S12..#.#.#...#
# ###3###.#.#.###
# ###4###.#.#...#
# ###5###.#.###.#
# ###6.E#...#...#
# ###.#######.###
# #...###...#...#
# #.#####.#.###.#
# #.#...#.#.#...#
# #.#.#.#.#.#.###
# #...#...#...###
# ###############
# Cheats don't need to use all 20 picoseconds; cheats can last any amount of time up to and including 20 picoseconds (but can still only end when the program is on normal track). Any cheat time not used is lost; it can't be saved for another cheat later.
#
# You'll still need a list of the best cheats, but now there are even more to choose between. Here are the quantities of cheats in this example that save 50 picoseconds or more:
#
# There are 32 cheats that save 50 picoseconds.
# There are 31 cheats that save 52 picoseconds.
# There are 29 cheats that save 54 picoseconds.
# There are 39 cheats that save 56 picoseconds.
# There are 25 cheats that save 58 picoseconds.
# There are 23 cheats that save 60 picoseconds.
# There are 20 cheats that save 62 picoseconds.
# There are 19 cheats that save 64 picoseconds.
# There are 12 cheats that save 66 picoseconds.
# There are 14 cheats that save 68 picoseconds.
# There are 12 cheats that save 70 picoseconds.
# There are 22 cheats that save 72 picoseconds.
# There are 4 cheats that save 74 picoseconds.
# There are 3 cheats that save 76 picoseconds.
# Find the best cheats using the updated cheating rules. How many cheats would save you at least 100 picoseconds?

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
        if rhs_time - lhs_time <= 20:
            continue

        manhattan_distance = abs(lhs_location[0] - rhs_location[0]) + abs(lhs_location[1] - rhs_location[1])
        
        if manhattan_distance <= 20:
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
