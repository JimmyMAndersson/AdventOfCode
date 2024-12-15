import os
import numpy as np
from itertools import product

# --- Part Two ---
# Fortunately, the Elves are trying to order so much fence that they qualify for a bulk discount!
#
# Under the bulk discount, instead of using the perimeter to calculate the price, you need to use the number of sides each region has. Each straight section of fence counts as a side, regardless of how long it is.
#
# Consider this example again:
#
# AAAA
# BBCD
# BBCC
# EEEC
# The region containing type A plants has 4 sides, as does each of the regions containing plants of type B, D, and E. However, the more complex region containing the plants of type C has 8 sides!
#
# Using the new method of calculating the per-region price by multiplying the region's area by its number of sides, regions A through E have prices 16, 16, 32, 4, and 12, respectively, for a total price of 80.
#
# The second example above (full of type X and O plants) would have a total price of 436.
#
# Here's a map that includes an E-shaped region full of type E plants:
#
# EEEEE
# EXXXX
# EEEEE
# EXXXX
# EEEEE
# The E-shaped region has an area of 17 and 12 sides for a price of 204. Including the two regions full of type X plants, this map has a total price of 236.
#
# This map has a total price of 368:
#
# AAAAAA
# AAABBA
# AAABBA
# ABBAAA
# ABBAAA
# AAAAAA
# It includes two regions full of type B plants (each with 4 sides) and a single region full of type A plants (with 4 sides on the outside and 8 more sides on the inside, a total of 12 sides). Be especially careful when counting the fence around regions like the one full of type A plants; in particular, each section of fence has an in-side and an out-side, so the fence does not connect across the middle of the region (where the two B regions touch diagonally). (The Elves would have used the Möbius Fencing Company instead, but their contract terms were too one-sided.)
#
# The larger example from before now has the following updated prices:
#
# A region of R plants with price 12 * 10 = 120.
# A region of I plants with price 4 * 4 = 16.
# A region of C plants with price 14 * 22 = 308.
# A region of F plants with price 10 * 12 = 120.
# A region of V plants with price 13 * 10 = 130.
# A region of J plants with price 11 * 12 = 132.
# A region of C plants with price 1 * 4 = 4.
# A region of E plants with price 13 * 8 = 104.
# A region of I plants with price 14 * 16 = 224.
# A region of M plants with price 5 * 6 = 30.
# A region of S plants with price 3 * 6 = 18.
# Adding these together produces its new total price of 1206.
#
# What is the new total price of fencing all regions on your map?

def count_sides(region):
    side_offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    neighbour_offsets = [((1, 0), (-1, 0)), ((1, 0), (-1, 0)), ((0, 1), (0, -1)), ((0, 1), (0, -1))]
    sides = []

    for side_offset, neighbour_offsets in zip(side_offsets, neighbour_offsets):
        side_points = set([point for point in region if (point[0] + side_offset[0], point[1] + side_offset[1]) not in region])

        while len(side_points) > 0:
            side = set()
            sides.append(side)
            queue = set([side_points.pop()])

            while len(queue) > 0:
                point = queue.pop()
                side.add(point)

                for neighbour_offset in neighbour_offsets:
                    neighbour = (point[0] + neighbour_offset[0], point[1] + neighbour_offset[1])
                    if neighbour in side_points and neighbour not in side:
                        queue.add(neighbour)
                        side_points.remove(neighbour)
        
    return len(sides)

if __name__ == '__main__':
    file_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(file_path)
    input_path = os.path.join(dir_path, 'input')
    
    with open(input_path, 'r') as file:
        data = [line.strip() for line in file.readlines()]
        data = np.array(data, dtype=str)
        data = data.view('U1').reshape(data.size, -1)

        rows = np.arange(data.shape[0])
        columns = np.arange(data.shape[1])

        not_categorized = set(product(rows, columns))
        regions = []
        adjoint_point_offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while len(not_categorized) > 0:
            region = set()
            start_point = not_categorized.pop()
            start_point_type = data[start_point]
            region.add(start_point)

            queue = set([
                (start_point[0] + i, start_point[1] + j) 
                for i, j 
                in adjoint_point_offsets 
                if (start_point[0] + i, start_point[1] + j) in not_categorized
            ])

            while len(queue) > 0:
                region_expanded = False
                point = queue.pop()
                if point in region:
                    continue
                if data[point] != start_point_type:
                    continue
                if point in not_categorized:
                    region.add(point)
                    not_categorized.remove(point)
                    for i, j in adjoint_point_offsets:
                        if (point[0] + i, point[1] + j) in not_categorized:
                            queue.add((point[0] + i, point[1] + j))

            regions.append(region)
        
        areas = np.array([len(region) for region in regions])
        sides = np.array([count_sides(region) for region in regions])

        print(areas @ sides)