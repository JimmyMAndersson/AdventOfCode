import os
from collections import defaultdict
import heapq
import numpy as np
from reindeer import Reindeer, Direction

# --- Part Two ---
# Now that you know what the best paths look like, you can figure out the best spot to sit.
#
# Every non-wall tile (S, ., or E) is equipped with places to sit along the edges of the tile. While determining which of these tiles would be the best spot to sit depends on a whole bunch of factors (how comfortable the seats are, how far away the bathrooms are, whether there's a pillar blocking your view, etc.), the most important factor is whether the tile is on one of the best paths through the maze. If you sit somewhere else, you'd miss all the action!
#
# So, you'll need to determine which tiles are part of any best path through the maze, including the S and E tiles.
#
# In the first example, there are 45 tiles (marked O) that are part of at least one of the various best paths through the maze:
#
# ###############
# #.......#....O#
# #.#.###.#.###O#
# #.....#.#...#O#
# #.###.#####.#O#
# #.#.#.......#O#
# #.#.#####.###O#
# #..OOOOOOOOO#O#
# ###O#O#####O#O#
# #OOO#O....#O#O#
# #O#O#O###.#O#O#
# #OOOOO#...#O#O#
# #O###.#.#.#O#O#
# #O..#.....#OOO#
# ###############
# In the second example, there are 64 tiles that are part of at least one of the best paths:
#
# #################
# #...#...#...#..O#
# #.#.#.#.#.#.#.#O#
# #.#.#.#...#...#O#
# #.#.#.#.###.#.#O#
# #OOO#.#.#.....#O#
# #O#O#.#.#.#####O#
# #O#O..#.#.#OOOOO#
# #O#O#####.#O###O#
# #O#O#..OOOOO#OOO#
# #O#O###O#####O###
# #O#O#OOO#..OOO#.#
# #O#O#O#####O###.#
# #O#O#OOOOOOO..#.#
# #O#O#O#########.#
# #O#OOO..........#
# #################
# Analyze your map further. How many tiles are part of at least one of the best paths through the maze?

if __name__ == '__main__':
    file_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(file_path)
    input_path = os.path.join(dir_path, 'input')
    
    with open(input_path, 'r') as file:
        data = [line.strip() for line in file.readlines()]
        data = np.array(data, dtype=str)
        data = data.view('U1').reshape(data.size, -1)
        starting_point = tuple(map(lambda x: x.item(), np.where(data == 'S')))
        walls = set(zip(*np.where(data == '#')))
        end_point = tuple(map(lambda x: x.item(), np.where(data == 'E')))

        reindeers = [
            Reindeer(
                location=starting_point,
                direction=Direction.EAST,
                path=set([starting_point]),
                score=0
            )
        ]

        min_tiles = set()
        tile_costs = defaultdict(lambda: float('inf'))
        min_score = float('inf')

        while len(reindeers) > 0:
            reindeer = heapq.heappop(reindeers)

            if reindeer.score > min_score:
                continue
            
            if tile_costs[(*reindeer.location, reindeer.direction)] < reindeer.score:
                continue

            tile_costs[(*reindeer.location, reindeer.direction)] = reindeer.score

            for direction, location in zip(Direction, reindeer.neighbor_tiles()):
                if (location[0], location[1]) in reindeer.path:
                    continue

                if location not in walls:
                    new_reindeer = Reindeer(
                        location=reindeer.location,
                        direction=reindeer.direction,
                        path=reindeer.path.copy(),
                        score=reindeer.score
                    )
                    new_reindeer.move(direction)

                    if new_reindeer.location == end_point:
                        if new_reindeer.score < min_score:
                            min_score = new_reindeer.score
                            min_tiles = new_reindeer.path.copy()
                        elif new_reindeer.score == min_score:
                            min_tiles |= new_reindeer.path
                        continue
                    
                    heapq.heappush(reindeers, new_reindeer)
        
        print(len(min_tiles))

