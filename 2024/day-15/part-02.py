import os
import numpy as np
from enum import Enum

# --- Part Two ---
# The lanternfish use your information to find a safe moment to swim in and turn off the malfunctioning robot! Just as they start preparing a festival in your honor, reports start coming in that a second warehouse's robot is also malfunctioning.
#
# This warehouse's layout is surprisingly similar to the one you just helped. There is one key difference: everything except the robot is twice as wide! The robot's list of movements doesn't change.
#
# To get the wider warehouse's map, start with your original map and, for each tile, make the following changes:
#
# If the tile is #, the new map contains ## instead.
# If the tile is O, the new map contains [] instead.
# If the tile is ., the new map contains .. instead.
# If the tile is @, the new map contains @. instead.
# This will produce a new warehouse map which is twice as wide and with wide boxes that are represented by []. (The robot does not change size.)
#
# The larger example from before would now look like this:
#
# ####################
# ##....[]....[]..[]##
# ##............[]..##
# ##..[][]....[]..[]##
# ##....[]@.....[]..##
# ##[]##....[]......##
# ##[]....[]....[]..##
# ##..[][]..[]..[][]##
# ##........[]......##
# ####################
# Because boxes are now twice as wide but the robot is still the same size and speed, boxes can be aligned such that they directly push two other boxes at once. For example, consider this situation:
#
# #######
# #...#.#
# #.....#
# #..OO@#
# #..O..#
# #.....#
# #######
#
# <vv<<^^<<^^
# After appropriately resizing this map, the robot would push around these boxes as follows:
#
# Initial state:
# ##############
# ##......##..##
# ##..........##
# ##....[][]@.##
# ##....[]....##
# ##..........##
# ##############
#
# Move <:
# ##############
# ##......##..##
# ##..........##
# ##...[][]@..##
# ##....[]....##
# ##..........##
# ##############
#
# Move v:
# ##############
# ##......##..##
# ##..........##
# ##...[][]...##
# ##....[].@..##
# ##..........##
# ##############
#
# Move v:
# ##############
# ##......##..##
# ##..........##
# ##...[][]...##
# ##....[]....##
# ##.......@..##
# ##############
#
# Move <:
# ##############
# ##......##..##
# ##..........##
# ##...[][]...##
# ##....[]....##
# ##......@...##
# ##############
#
# Move <:
# ##############
# ##......##..##
# ##..........##
# ##...[][]...##
# ##....[]....##
# ##.....@....##
# ##############
#
# Move ^:
# ##############
# ##......##..##
# ##...[][]...##
# ##....[]....##
# ##.....@....##
# ##..........##
# ##############
#
# Move ^:
# ##############
# ##......##..##
# ##...[][]...##
# ##....[]....##
# ##.....@....##
# ##..........##
# ##############
#
# Move <:
# ##############
# ##......##..##
# ##...[][]...##
# ##....[]....##
# ##....@.....##
# ##..........##
# ##############
#
# Move <:
# ##############
# ##......##..##
# ##...[][]...##
# ##....[]....##
# ##...@......##
# ##..........##
# ##############
#
# Move ^:
# ##############
# ##......##..##
# ##...[][]...##
# ##...@[]....##
# ##..........##
# ##..........##
# ##############
#
# Move ^:
# ##############
# ##...[].##..##
# ##...@.[]...##
# ##....[]....##
# ##..........##
# ##..........##
# ##############
# This warehouse also uses GPS to locate the boxes. For these larger boxes, distances are measured from the edge of the map to the closest edge of the box in question. So, the box shown below has a distance of 1 from the top edge of the map and 5 from the left edge of the map, resulting in a GPS coordinate of 100 * 1 + 5 = 105.
#
# ##########
# ##...[]...
# ##........
# In the scaled-up version of the larger example from above, after the robot has finished all of its moves, the warehouse would look like this:
#
# ####################
# ##[].......[].[][]##
# ##[]...........[].##
# ##[]........[][][]##
# ##[]......[]....[]##
# ##..##......[]....##
# ##..[]............##
# ##..@......[].[][]##
# ##......[][]..[]..##
# ####################
# The sum of these boxes' GPS coordinates is 9021.
#
# Predict the motion of the robot and boxes in this new, scaled-up warehouse. What is the sum of all boxes' final GPS coordinates?

class Direction(Enum):
    UP = '^'
    DOWN = 'v'
    LEFT = '<'
    RIGHT = '>'

    def next_idx(self, idx):
        if self == Direction.UP:
            return (idx[0] - 1, idx[1])
        elif self == Direction.DOWN:
            return (idx[0] + 1, idx[1])
        elif self == Direction.LEFT:
            return (idx[0], idx[1] - 1)
        elif self == Direction.RIGHT:
            return (idx[0], idx[1] + 1)
    
    def prev_idx(self, idx):
        if self == Direction.UP:
            return (idx[0] + 1, idx[1])
        elif self == Direction.DOWN:
            return (idx[0] - 1, idx[1])
        elif self == Direction.LEFT:
            return (idx[0], idx[1] + 1)
        elif self == Direction.RIGHT:
            return (idx[0], idx[1] - 1)

def remap_warehouse(map):
    new_map = []
    for row in map:
        new_row = ''
        for tile in row:
            if tile == '#':
                new_row += '##'
            elif tile == 'O':
                new_row += '[]'
            elif tile == '.':
                new_row += '..'
            elif tile == '@':
                new_row += '@.'
        new_map.append(new_row)
    return new_map

def is_moveable(warehouse, idx, direction):
    queue = {idx}
    visited = set()
    while len(queue) > 0:
        idx = queue.pop()
        if idx in visited:
            continue
        else:
            visited.add(idx)
        
        next_idx = direction.next_idx(idx)
        
        if warehouse[next_idx] == '#':
            return False
        elif warehouse[next_idx] == '.':
            continue
        elif warehouse[next_idx] == '[':
            other_box_idx = (next_idx[0], next_idx[1] + 1)
            queue.add(next_idx)
            queue.add(other_box_idx)
        elif warehouse[next_idx] == ']':
            other_box_idx = (next_idx[0], next_idx[1] - 1)
            queue.add(next_idx)
            queue.add(other_box_idx)
    
    return True

def move(warehouse, idx, new_tile, direction, visited):
    if idx in visited:
        return
    else:
        visited.add(idx)
    
    next_idx = direction.next_idx(idx)
    if warehouse[next_idx] == '.':
        warehouse[next_idx] = warehouse[idx]
        warehouse[idx] = new_tile
    elif warehouse[next_idx] == '[':
        other_box_idx = (next_idx[0], next_idx[1] + 1)

        move(warehouse, next_idx, warehouse[idx], direction, visited)
        move(warehouse, other_box_idx, '.', direction, visited)
        warehouse[idx] = new_tile
    elif warehouse[next_idx] == ']':
        other_box_idx = (next_idx[0], next_idx[1] - 1)

        move(warehouse, next_idx, warehouse[idx], direction, visited)
        move(warehouse, other_box_idx, '.', direction, visited)
        warehouse[idx] = new_tile

if __name__ == '__main__':
    file_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(file_path)
    input_path = os.path.join(dir_path, 'input')
    
    with open(input_path, 'r') as file:
        data = file.read().split('\n\n')
        warehouse = data[0].split('\n')
        warehouse = remap_warehouse(warehouse)
        warehouse = np.array(warehouse, dtype=str).view('U1').reshape(len(warehouse), -1)
        moves = data[1].replace('\n', '')

        for move_idx, mv in enumerate(moves):
            direction = Direction(mv)
            robot_position = np.where(warehouse == '@')

            robot_position = (robot_position[0][0], robot_position[1][0])
            
            if is_moveable(warehouse, robot_position, direction):
                move(warehouse, robot_position, '.', direction, set())
        
        box_idx = np.where(warehouse == '[')
        gps_coordinates = 100 * box_idx[0] + box_idx[1]
        print(gps_coordinates.sum())