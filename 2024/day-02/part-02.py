import numpy as np
import os

# --- Part Two ---
# The engineers are surprised by the low number of safe reports until they realize they forgot to tell you about the Problem Dampener.
#
# The Problem Dampener is a reactor-mounted module that lets the reactor safety systems tolerate a single bad level in what would otherwise be a safe report. It's like the bad level never happened!
#
# Now, the same rules apply as before, except if removing a single level from an unsafe report would make it safe, the report instead counts as safe.
#
# More of the above example's reports are now safe:
#
# 7 6 4 2 1: Safe without removing any level.
# 1 2 7 8 9: Unsafe regardless of which level is removed.
# 9 7 6 2 1: Unsafe regardless of which level is removed.
# 1 3 2 4 5: Safe by removing the second level, 3.
# 8 6 4 4 1: Safe by removing the third level, 4.
# 1 3 6 7 9: Safe without removing any level.
# Thanks to the Problem Dampener, 4 reports are actually safe!
#
# Update your analysis by handling situations where the Problem Dampener can remove a single level from unsafe reports. How many reports are now safe?

# write a function that takes in a list of integers and returns a boolean indicating whether the list is safe
# a list is safe if it is monotonically increasing or decreasing and the difference between each element is less than or equal to 3
def is_safe(nums):
    diffs = nums[1:] - nums[:-1]
    monotonically_changing = np.all(diffs > 0) or np.all(diffs < 0)
    diff_range = np.all(np.abs(diffs) <= 3)
    return monotonically_changing and diff_range

if __name__ == '__main__':
    file_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(file_path)
    input_path = os.path.join(dir_path, 'input')

    num_safe_reports = 0

    with open(input_path, 'r') as input_file:
        for line in input_file:
            nums = np.array(line.split(' '), dtype=int)

            for index in range(-1, nums.shape[0]):
                if is_safe(np.delete(nums, index)):
                    num_safe_reports += 1
                    break

    print(num_safe_reports)