import numpy as np
import os
from functools import partial

# --- Day 4: Ceres Search ---
# "Looks like the Chief's not here. Next!" One of The Historians pulls out a device and pushes the only button on it. After a brief flash, you recognize the interior of the Ceres monitoring station!
#
# As the search for the Chief continues, a small Elf who lives on the station tugs on your shirt; she'd like to know if you could help her with her word search (your puzzle input). She only has to find one word: XMAS.
#
# This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to find all of them. Here are a few ways XMAS might appear, where irrelevant characters have been replaced with .:
#
#
# ..X...
# .SAMX.
# .A..A.
# XMAS.S
# .X....
# The actual word search will be full of letters instead. For example:
#
# MMMSXXMASM
# MSAMXMSMSA
# AMXSXMAAMM
# MSAMASMSMX
# XMASAMXAMM
# XXAMMXXAMA
# SMSMSASXSS
# SAXAMASAAA
# MAMMMXMMMM
# MXMXAXMASX
# In this word search, XMAS occurs a total of 18 times; here's the same word search again, but where letters not involved in any XMAS have been replaced with .:
#
# ....XXMAS.
# .SAMXMS...
# ...S..A...
# ..A.A.MS.X
# XMASAMX.MM
# X.....XA.A
# S.S.S.S.SS
# .A.A.A.A.A
# ..M.M.M.MM
# .X.X.XMASX
# Take a look at the little Elf's word search. How many times does XMAS appear?

def find_horizontal_and_main_diagonal(matrix, word):
    rev_word = np.flip(word)

    count = 0
    # Match all words along the horizontal axis
    for column in np.arange(0, matrix.shape[1] - word.shape[0] + 1):
        sub_matrix = matrix[:, column:column + word.shape[0]]
        count += np.sum(np.all(sub_matrix == word, axis=1), axis=0)
        count += np.sum(np.all(sub_matrix == rev_word, axis=1), axis=0)
    
    # Match all words along the main diagonal
    for row in np.arange(0, matrix.shape[0] - word.shape[0] + 1):
        for column in np.arange(0, matrix.shape[1] - word.shape[0] + 1):
            sub_matrix = matrix[row:row + word.shape[0], column:column + word.shape[0]]
            count += np.sum(np.all(np.diag(sub_matrix) == word))
            count += np.sum(np.all(np.diag(sub_matrix) == rev_word))
    
    return count

if __name__ == '__main__':
    file_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(file_path)
    input_path = os.path.join(dir_path, 'input')

    with open(input_path, 'r') as file:
        data = [line.strip() for line in file.readlines()]
        data = np.array(data, dtype=str)
        data = data.view('U1').reshape(data.size, -1)

        XMAS = np.array(['XMAS'], dtype=str).view('U1')
        SAMX = np.flip(XMAS)

        matcher_transform_funcs = [
            partial(find_horizontal_and_main_diagonal, matrix=data, word=XMAS),
            partial(find_horizontal_and_main_diagonal, matrix=np.rot90(data, k=1), word=XMAS)
        ]
        result = np.sum([matcher() for matcher in matcher_transform_funcs])
        print(result)
