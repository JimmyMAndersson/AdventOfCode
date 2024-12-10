import os
import numpy as np

# --- Part Two ---
# Upon completion, two things immediately become clear. First, the disk definitely has a lot more contiguous free space, just like the amphipod hoped. Second, the computer is running much more slowly! Maybe introducing all of that file system fragmentation was a bad idea?
#
# The eager amphipod already has a new plan: rather than move individual blocks, he'd like to try compacting the files on his disk by moving whole files instead.
#
# This time, attempt to move whole files to the leftmost span of free space blocks that could fit the file. Attempt to move each file exactly once in order of decreasing file ID number starting with the file with the highest file ID number. If there is no span of free space to the left of a file that is large enough to fit the file, the file does not move.
#
# The first example from above now proceeds differently:
#
# 00...111...2...333.44.5555.6666.777.888899
# 0099.111...2...333.44.5555.6666.777.8888..
# 0099.1117772...333.44.5555.6666.....8888..
# 0099.111777244.333....5555.6666.....8888..
# 00992111777.44.333....5555.6666.....8888..
# The process of updating the filesystem checksum is the same; now, this example's checksum would be 2858.
#
# Start over, now compacting the amphipod's hard drive using this new method instead. What is the resulting filesystem checksum?

def expand_diskmap(diskmap: str):
    file_system = []
    current_block = 0
    for idx, blocks in enumerate(diskmap):
        if idx & 1:
            file_system.append([-1, current_block, int(blocks)])
        else:
            file_system.append([idx // 2, current_block, int(blocks)])
        
        current_block += int(blocks)
    
    return file_system

def rearrange_file_system(file_system):
    for file_idx in np.arange(len(file_system) - 1, -1, -2):
        for space_idx in np.arange(1, file_idx, 2):
            if file_system[file_idx][2] <= file_system[space_idx][2]:
                file_system[file_idx][1] = file_system[space_idx][1]
                file_system[space_idx][1] += file_system[file_idx][2]
                file_system[space_idx][2] -= file_system[file_idx][2]
                break
    
    return file_system

if __name__ == '__main__':
    file_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(file_path)
    input_path = os.path.join(dir_path, 'input')

    with open(input_path, 'r') as file:
        diskmap = file.read().strip()
        file_system = expand_diskmap(diskmap)
        file_system = rearrange_file_system(file_system)
        
        checksum = 0
        for file_idx in np.arange(0, len(file_system), 2):
            [file_id, file_start_idx, file_length] = file_system[file_idx]
            file_end_idx = file_start_idx + file_length
            block_weight_sum = int((file_end_idx * (file_end_idx - 1) - file_start_idx * (file_start_idx - 1)) / 2)
            checksum += block_weight_sum * file_id

    print(checksum)