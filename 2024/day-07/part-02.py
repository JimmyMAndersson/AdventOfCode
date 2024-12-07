import os
import numpy as np
import multiprocessing as mp

# --- Part Two ---
# The engineers seem concerned; the total calibration result you gave them is nowhere close to being within safety tolerances. Just then, you spot your mistake: some well-hidden elephants are holding a third type of operator.
#
# The concatenation operator (||) combines the digits from its left and right inputs into a single number. For example, 12 || 345 would become 12345. All operators are still evaluated left-to-right.
#
# Now, apart from the three equations that could be made true using only addition and multiplication, the above example has three more equations that can be made true by inserting operators:
#
# 156: 15 6 can be made true through a single concatenation: 15 || 6 = 156.
# 7290: 6 8 6 15 can be made true using 6 * 8 || 6 * 15.
# 192: 17 8 14 can be made true using 17 || 8 + 14.
# Adding up all six test values (the three that could be made before using only + and * plus the new three that can now be made by also using ||) produces the new total calibration result of 11387.
#
# Using your new knowledge of elephant hiding spots, determine which equations could possibly be true. What is their total calibration result?

def is_possible_equation(test_value: int, current_value: int, remaining_numbers: np.array) -> bool:
    if remaining_numbers.size == 0:
        return test_value == current_value
    
    if test_value < current_value:
        return False
    
    return (
        is_possible_equation(test_value, current_value + remaining_numbers[0], remaining_numbers[1:]) or
        is_possible_equation(test_value, current_value * remaining_numbers[0], remaining_numbers[1:]) or
        is_possible_equation(test_value, int(str(current_value) + str(remaining_numbers[0])), remaining_numbers[1:])
    )
    

if __name__ == '__main__':
    file_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(file_path)
    input_path = os.path.join(dir_path, 'input')
    
    with open(input_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]

        equations = [
            (int(line[0]), np.array(line[1].split(' '), dtype=int))
            for line
            in [
                line.split(': ')
                for line 
                in lines
            ]
        ]

        with mp.Pool() as pool:
            results = pool.starmap(
                is_possible_equation,
                [
                    (test_value, 0, remaining_numbers)
                    for test_value, remaining_numbers
                    in equations
                ]
            )

        valid_test_values = np.array([test_value for test_value, _ in equations])[results]
        print(np.sum(valid_test_values))
