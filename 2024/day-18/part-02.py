import os
import re
from collections import defaultdict
from queue import PriorityQueue
from tile import Tile

# --- Part Two ---
# The Historians aren't as used to moving around in this pixelated universe as you are. You're afraid they're not going to be fast enough to make it to the exit before the path is completely blocked.
#
# To determine how fast everyone needs to go, you need to determine the first byte that will cut off the path to the exit.
#
# In the above example, after the byte at 1,1 falls, there is still a path to the exit:
#
# O..#OOO
# O##OO#O
# O#OO#OO
# OOO#OO#
# ###OO##
# .##O###
# #.#OOOO
# However, after adding the very next byte (at 6,1), there is no longer a path to the exit:
#
# ...#...
# .##..##
# .#..#..
# ...#..#
# ###..##
# .##.###
# #.#....
# So, in this example, the coordinates of the first byte that prevents the exit from being reachable are 6,1.
#
# Simulate more of the bytes that are about to corrupt your memory space. What are the coordinates of the first byte that will prevent the exit from being reachable from your starting position? (Provide the answer as two integers separated by a comma with no other characters.)

if __name__ == '__main__':
    file_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(file_path)
    input_path = os.path.join(dir_path, 'input')
    
    with open(input_path, 'r') as file:
        data = re.findall(r'(\d+),(\d+)', file.read().strip())
        falling_bytes = [(int(x), int(y)) for x, y in data]

        end_coordinates = (70, 70)

        for idx in range(1, len(falling_bytes)):
            bytes = falling_bytes[:idx]
            byte_set = set(falling_bytes[:idx])
            visited = defaultdict(lambda: float('inf'))
            queue = PriorityQueue()
            queue.put(Tile((0, 0), 0))

            while not queue.empty():
                tile = queue.get()
                x, y = tile.location

                if tile.location == end_coordinates:
                    break

                for neighbor in tile.neighbors():
                    if visited[neighbor.location] > neighbor.distance and neighbor.location not in byte_set:
                        visited[neighbor.location] = neighbor.distance
                        queue.put(neighbor)
            else:
                print(bytes[-1])
                break
