import os
import re

# --- Part Two ---
# Digging deeper in the device's manual, you discover the problem: this program is supposed to output another copy of the program! Unfortunately, the value in register A seems to have been corrupted. You'll need to find a new value to which you can initialize register A so that the program's output instructions produce an exact copy of the program itself.
#
# For example:
#
# Register A: 2024
# Register B: 0
# Register C: 0
#
# Program: 0,3,5,4,3,0
# This program outputs a copy of itself if register A is instead initialized to 117440. (The original initial value of register A, 2024, is ignored.)
#
# What is the lowest positive initial value for register A that causes the program to output a copy of itself?

def combo(operand, registers):
    if operand < 4:
        return operand
    elif operand == 4:
        return registers['A']
    elif operand == 5:
        return registers['B']
    elif operand == 6:
        return registers['C']
    else:
        return None

def run_program(program, initial_a_register):
    registers = {
        'A': initial_a_register,
        'B': 0,
        'C': 0
    }

    pointer = 0
    output = []
    
    while pointer < len(program):
        [opcode, operand] = program[pointer:pointer + 2]
        pointer += 2
        
        if opcode == 0:
            registers['A'] //= 2 ** combo(operand, registers)
        elif opcode == 1:
            registers['B'] ^= operand
        elif opcode == 2:
            registers['B'] = combo(operand, registers) & 0b111
        elif opcode == 3:
            pointer = pointer if registers['A'] == 0 else operand
        elif opcode == 4:
            registers['B'] ^= registers['C']
        elif opcode == 5:
            output.append(combo(operand, registers) & 0b111)
        elif opcode == 6:
            registers['B'] = registers['A'] // (2 ** combo(operand, registers))
        elif opcode == 7:
            registers['C'] = registers['A'] // (2 ** combo(operand, registers))
    
    return output
    
def find_next(program, target, initial_a_register = 0):
    if target == []:
        return initial_a_register
    for candidate in ((initial_a_register << 3) + new_3_bits for new_3_bits in range(8)):
        if run_program(program, candidate).pop() == target[-1]:
            try:
                return find_next(program, target[:-1], candidate)
            except StopIteration:
                continue
    raise StopIteration

if __name__ == '__main__':
    file_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(file_path)
    input_path = os.path.join(dir_path, 'input')
    
    with open(input_path, 'r') as file:
        data = file.read().strip().split('\n\n')
        program_pattern = r'(?P<op>\d+),?'
        program = list(map(int, re.findall(program_pattern, data[1])))
        
        initial_a = find_next(program[:-2], program, 0)
        print(initial_a)
