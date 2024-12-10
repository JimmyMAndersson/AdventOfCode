import os
import numpy as np
from functools import partial

# --- Part Two ---
# The reindeer spends a few minutes reviewing your hiking trail map before realizing something, disappearing for a few minutes, and finally returning with yet another slightly-charred piece of paper.
#
# The paper describes a second way to measure a trailhead called its rating. A trailhead's rating is the number of distinct hiking trails which begin at that trailhead. For example:
#
# .....0.
# ..4321.
# ..5..2.
# ..6543.
# ..7..4.
# ..8765.
# ..9....
# The above map has a single trailhead; its rating is 3 because there are exactly three distinct hiking trails which begin at that position:
#
# .....0.   .....0.   .....0.
# ..4321.   .....1.   .....1.
# ..5....   .....2.   .....2.
# ..6....   ..6543.   .....3.
# ..7....   ..7....   .....4.
# ..8....   ..8....   ..8765.
# ..9....   ..9....   ..9....
# Here is a map containing a single trailhead with rating 13:
#
# ..90..9
# ...1.98
# ...2..7
# 6543456
# 765.987
# 876....
# 987....
# This map contains a single trailhead with rating 227 (because there are 121 distinct hiking trails that lead to the 9 on the right edge and 106 that lead to the 9 on the bottom edge):
#
# 012345
# 123456
# 234567
# 345678
# 4.6789
# 56789.
# Here's the larger example from before:
#
# 89010123
# 78121874
# 87430965
# 96549874
# 45678903
# 32019012
# 01329801
# 10456732
# Considering its trailheads in reading order, they have ratings of 20, 24, 10, 4, 1, 4, 5, 8, and 5. The sum of all trailhead ratings in this larger example topographic map is 81.
#
# You're not sure how, but the reindeer seems to have crafted some tiny flags out of toothpicks and bits of paper and is using them to mark trailheads on your topographic map. What is the sum of the ratings of all trailheads?

def count_distinct_paths(last_location, data, last_height):
    row, col = last_location
    row_min = np.maximum(0, row - 1)
    row_max = np.minimum(data.shape[0] - 1, row + 1)
    col_min = np.maximum(0, col - 1)
    col_max = np.minimum(data.shape[1] - 1, col + 1)

    mask = np.zeros_like(data, dtype=bool)
    mask[row, col_min] = True
    mask[row, col_max] = True
    mask[row_min, col] = True
    mask[row_max, col] = True
    mask[row, col] = False
    
    next_steps = np.nonzero((data == last_height + 1) & mask)
    
    if last_height + 1 == 9:
        return next_steps[0].size
    else:
        searcher = partial(count_distinct_paths, data=data, last_height=last_height + 1)
        mapper = map(searcher, zip(*next_steps))
        return np.sum(list(mapper), dtype=int)

if __name__ == '__main__':
    file_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(file_path)
    input_path = os.path.join(dir_path, 'input')
    
    with open(input_path, 'r') as file:
        data = [line.strip() for line in file.readlines()]
        data = np.array(data, dtype=str)
        data = data.view('U1').reshape(data.size, -1).astype(int)

        starting_points = np.nonzero(data == 0)
        searcher = partial(count_distinct_paths, data=data, last_height=0)
        path_count = np.sum(list(map(searcher, zip(*starting_points))), dtype=int)

        print(path_count)
