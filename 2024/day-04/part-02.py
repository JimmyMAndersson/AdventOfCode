import numpy as np
import os
from functools import partial

# --- Part Two ---
# The Elf looks quizzically at you. Did you misunderstand the assignment?
#
# Looking for the instructions, you flip over the word search to find that this isn't actually an XMAS puzzle; it's an X-MAS puzzle in which you're supposed to find two MAS in the shape of an X. One way to achieve that is like this:
#
# M.S
# .A.
# M.S
# Irrelevant characters have again been replaced with . in the above diagram. Within the X, each MAS can be written forwards or backwards.
#
# Here's the same example from before, but this time all of the X-MASes have been kept instead:
#
# .M.S......
# ..A..MSMS.
# .M.S.MAA..
# ..A.ASMSM.
# .M.S.M....
# ..........
# S.S.S.S.S.
# .A.A.A.A..
# M.M.M.M.M.
# ..........
# In this example, an X-MAS appears 9 times.
#
# Flip the word search from the instructions back over to the word search side and try again. How many times does an X-MAS appear?

def find_X(matrix, main_diagnoal_word, antidiagonal_word):
    assert main_diagnoal_word.shape == antidiagonal_word.shape, 'First and second word must have the same shape'
    count = 0

    for row in np.arange(0, matrix.shape[0] - main_diagnoal_word.shape[0] + 1):
        for column in np.arange(0, matrix.shape[1] - main_diagnoal_word.shape[0] + 1):
            sub_matrix = matrix[row:row + main_diagnoal_word.shape[0], column:column + main_diagnoal_word.shape[0]]

            main_diagonal_match = np.all(np.diag(sub_matrix) == main_diagnoal_word)
            antidiagonal_match = np.all(np.diag(np.rot90(sub_matrix, k=1)) == antidiagonal_word)
            
            count += np.sum(main_diagonal_match and antidiagonal_match)
    
    return count

if __name__ == '__main__':
    file_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(file_path)
    input_path = os.path.join(dir_path, 'input')

    with open(input_path, 'r') as file:
        data = [line.strip() for line in file.readlines()]
        data = np.array(data, dtype=str)
        data = data.view('U1').reshape(data.size, -1)

        MAS = np.array(['MAS'], dtype=str).view('U1')
        SAM = np.flip(MAS)

        matcher_funcs = [
            partial(find_X, matrix=data, main_diagnoal_word=MAS, antidiagonal_word=MAS),
            partial(find_X, matrix=data, main_diagnoal_word=MAS, antidiagonal_word=SAM),
            partial(find_X, matrix=data, main_diagnoal_word=SAM, antidiagonal_word=MAS),
            partial(find_X, matrix=data, main_diagnoal_word=SAM, antidiagonal_word=SAM),
        ]
        result = np.sum([matcher() for matcher in matcher_funcs])
        print(result)
