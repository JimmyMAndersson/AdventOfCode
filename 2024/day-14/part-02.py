import os
import re
from collections import defaultdict

# --- Part Two ---
# During the bathroom break, someone notices that these robots seem awfully similar to ones built and used at the North Pole. If they're the same type of robots, they should have a hard-coded Easter egg: very rarely, most of the robots should arrange themselves into a picture of a Christmas tree.
#
# What is the fewest number of seconds that must elapse for the robots to display the Easter egg?

if __name__ == '__main__':
    file_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(file_path)
    input_path = os.path.join(dir_path, 'input')
    
    with open(input_path, 'r') as file:
        regex = r'p=(?P<x>\d+),(?P<y>\d+) v=(?P<vx>-?\d+),(?P<vy>-?\d+)'
        data = file.readlines()

        robots = {
            (int(x), int(y), int(vx), int(vy))
            for line in data
            for x, y, vx, vy in re.findall(regex, line)
        }
        width = 101
        height = 103
        seconds = 0
        done = False

        while not done:
            seconds += 1
            robots = {
                ((x + vx) % width, (y + vy) % height, vx, vy)
                for x, y, vx, vy in robots
            }

            row_groups = defaultdict(list)
            for x, y, _, _ in robots:
                row_groups[x].append(y)
            
            for group in row_groups.values():
                if len(group) >= 10:
                    group.sort()
                    consecutive = 0
                    for i in range(1, len(group)):
                        if group[i] - group[i - 1] == 1:
                            consecutive += 1
                        else:
                            consecutive = 0
                        if consecutive == 9:
                            done = True
                            break
                    else:
                        continue
                    break
        
        print(seconds)