import os
import numpy as np

# --- Part Two ---
# Watching over your shoulder as you work, one of The Historians asks if you took the effects of resonant harmonics into your calculations.
#
# Whoops!
#
# After updating your model, it turns out that an antinode occurs at any grid position exactly in line with at least two antennas of the same frequency, regardless of distance. This means that some of the new antinodes will occur at the position of each antenna (unless that antenna is the only one of its frequency).
#
# So, these three T-frequency antennas now create many antinodes:
#
# T....#....
# ...T......
# .T....#...
# .........#
# ..#.......
# ..........
# ...#......
# ..........
# ....#.....
# ..........
# In fact, the three T-frequency antennas are all exactly in line with two antennas, so they are all also antinodes! This brings the total number of antinodes in the above example to 9.
#
# The original example now has 34 antinodes, including the antinodes that appear on every antenna:
#
# ##....#....#
# .#.#....0...
# ..#.#0....#.
# ..##...0....
# ....0....#..
# .#...#A....#
# ...#..#.....
# #....#.#....
# ..#.....A...
# ....#....A..
# .#........#.
# ...#......##
# Calculate the impact of the signal using this updated model. How many unique locations within the bounds of the map contain an antinode?

if __name__ == '__main__':
    file_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(file_path)
    input_path = os.path.join(dir_path, 'input')
    
    with open(input_path, 'r') as file:
        data = [line.strip() for line in file.readlines()]
        data = np.array(data, dtype=str)
        data = data.view('U1').reshape(data.size, -1)

        antennae = np.unique(data)
        antennae = antennae[antennae != '.']
        
        antennae_locations = { antenna: np.argwhere(data == antenna) for antenna in antennae }
        antinodes = set()

        map_shape = data.shape

        for antenna, locations in antennae_locations.items():
            for i, location in enumerate(locations):
                for j, other_location in enumerate(locations[i+1:]):
                    distance = location - other_location

                    for counter in np.arange(0, np.max(map_shape)):
                        antinode = location + counter * distance
                        if 0 <= antinode[0] < map_shape[0] and 0 <= antinode[1] < map_shape[1]:
                            antinodes.add(tuple(antinode))
                        else:
                            break

                    for counter in np.arange(0, np.max(map_shape)):
                        antinode = other_location - counter * distance
                        if 0 <= antinode[0] < map_shape[0] and 0 <= antinode[1] < map_shape[1]:
                            antinodes.add(tuple(antinode))
                        else:
                            break
        
        print(len(antinodes))
