import os
import numpy as np
from numpy.linalg import solve
import re

# --- Part Two ---
# As you go to win the first prize, you discover that the claw is nowhere near where you expected it would be. Due to a unit conversion error in your measurements, the position of every prize is actually 10000000000000 higher on both the X and Y axis!
#
# Add 10000000000000 to the X and Y position of every prize. After making this change, the example above would now look like this:
#
# Button A: X+94, Y+34
# Button B: X+22, Y+67
# Prize: X=10000000008400, Y=10000000005400
#
# Button A: X+26, Y+66
# Button B: X+67, Y+21
# Prize: X=10000000012748, Y=10000000012176
#
# Button A: X+17, Y+86
# Button B: X+84, Y+37
# Prize: X=10000000007870, Y=10000000006450
#
# Button A: X+69, Y+23
# Button B: X+27, Y+71
# Prize: X=10000000018641, Y=10000000010279
# Now, it is only possible to win a prize on the second and fourth claw machines. Unfortunately, it will take many more than 100 presses to do so.
#
# Using the corrected prize coordinates, figure out how to win as many prizes as possible. What is the fewest tokens you would have to spend to win all possible prizes?

if __name__ == '__main__':
    file_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(file_path)
    input_path = os.path.join(dir_path, 'input')
    
    with open(input_path, 'r') as file:
        data = file.read().strip().split('\n\n')
        print(len(data))
        button_regex = r'X\+(\d+), Y\+(\d+)'
        prize_regex = r'X=(\d+), Y=(\d+)'
        button_tokens = np.array([3, 1])

        total_tokens = 0
        conv_error = int(10000000000000)
        
        for claw_machine in data:
            button_steps = np.array([(int(x[0]), int(x[1])) for x in re.findall(button_regex, claw_machine)]).transpose()
            prize_location = np.array([(int(x[0]), int(x[1])) for x in re.findall(prize_regex, claw_machine)]).squeeze()
            prize_location += conv_error
            result = solve(button_steps, prize_location).round()
            total_tokens += int(button_tokens @ result) if (button_steps @ result == prize_location).all() else 0
        
        print(total_tokens)
