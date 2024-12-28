import os
from keypad import find_numpad_path, find_dirpad_path
import re

# --- Part Two ---
# Just as the missing Historian is released, The Historians realize that a second member of their search party has also been missing this entire time!
#
# A quick life-form scan reveals the Historian is also trapped in a locked area of the ship. Due to a variety of hazards, robots are once again dispatched, forming another chain of remote control keypads managing robotic-arm-wielding robots.
#
# This time, many more robots are involved. In summary, there are the following keypads:
#
# One directional keypad that you are using.
# 25 directional keypads that robots are using.
# One numeric keypad (on a door) that a robot is using.
# The keypads form a chain, just like before: your directional keypad controls a robot which is typing on a directional keypad which controls a robot which is typing on a directional keypad... and so on, ending with the robot which is typing on the numeric keypad.
#
# The door codes are the same this time around; only the number of robots and directional keypads has changed.
#
# Find the fewest number of button presses you'll need to perform in order to cause the robot in front of the door to type each code. What is the sum of the complexities of the five codes on your list?

if __name__ == '__main__':
    file_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(file_path)
    input_path = os.path.join(dir_path, 'input')
    
    with open(input_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
        number_regex = r'^\d+'

        complexity = 0

        for idx, line in enumerate(lines):
            result = 0
            for code in find_numpad_path(line):
                result += find_dirpad_path(code, n=25)
            complexity += int(re.match(number_regex, line).group(0)) * result

        print(complexity)
