import os
import numpy as np
from collections import defaultdict

# --- Part Two ---
# The Historians sure are taking a long time. To be fair, the infinite corridors are very large.
#
# How many stones would you have after blinking a total of 75 times?

if __name__ == '__main__':
    file_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(file_path)
    input_path = os.path.join(dir_path, 'input')
    
    with open(input_path, 'r') as file:
        data = file.read().strip().split()
        data = np.array(data, dtype=int)
        stones = defaultdict(int)

        for num in data:
            stones[num] += 1
        
        for _ in range(75):
            new_stones = defaultdict(int)
            for stone, count in stones.items():
                if stone == 0:
                    new_stones[1] += count
                elif not len(str(stone)) & 1:
                    stone_str = str(stone)
                    half = len(stone_str) // 2
                    new_stones[int(stone_str[:half])] += count
                    new_stones[int(stone_str[half:])] += count
                else:
                    new_stones[stone * 2024] += count
            
            stones = new_stones
            
        print(np.sum(list(stones.values())))
        
