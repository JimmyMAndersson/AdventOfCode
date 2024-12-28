from functools import lru_cache

def left_right(diff):
    if diff[1] < 0:
        return ((1, 0),) * abs(diff[1])
    elif diff[1] > 0:
        return ((1, 2),) * diff[1]
    else:
        return ()

def up_down(diff):
    if diff[0] < 0:
        return ((0, 1),) * abs(diff[0])
    elif diff[0] > 0:
        return ((1, 1),) * diff[0]
    else:
        return ()

def diff(start, end):
    return (end[0] - start[0], end[1] - start[1])
    
def find_numpad_path(code):
    lhs = map(numpad_positions.get, 'A' + code[:-1])
    rhs = map(numpad_positions.get, code)
    return tuple(map(expand_numpad_path, zip(lhs, rhs)))

numpad_positions = {
    '7': (0, 0),
    '8': (0, 1),
    '9': (0, 2),
    '4': (1, 0),
    '5': (1, 1),
    '6': (1, 2),
    '1': (2, 0),
    '2': (2, 1),
    '3': (2, 2),
    '0': (3, 1),
    'A': (3, 2)
}

def expand_numpad_path(pair):
    start, end = pair
    dxy = diff(start, end)

    if start[0] == 3 and end[1] == 0:
        return up_down(dxy) + left_right(dxy) + ((0, 2),)
    elif start[1] == 0 and end[0] == 3:
        return left_right(dxy) + up_down(dxy) + ((0, 2),)
    elif dxy[1] < 0:
        return left_right(dxy) + up_down(dxy) + ((0, 2),)
    else:
        return up_down(dxy) + left_right(dxy) + ((0, 2),)

@lru_cache(maxsize=1_000)
def find_dirpad_path(code, n):
    if n == 0:
        return len(code)
    
    result = 0
    lhs = ((0, 2),) + code[:-1]
    rhs = code
    
    for path in list(map(expand_dirpad_path, zip(lhs, rhs))):
        result += find_dirpad_path(path, n - 1)
    
    return result

dirpad_positions = {
    '^': (0, 1),
    'A': (0, 2),
    '<': (1, 0),
    'v': (1, 1),
    '>': (1, 2)
}

def expand_dirpad_path(pair):
    start, end = pair
    dxy = diff(start, end)

    if start == dirpad_positions['<']:
        return left_right(dxy) + up_down(dxy) + ((0, 2),)
    elif end == dirpad_positions['<']:
        return up_down(dxy) + left_right(dxy) + ((0, 2),)
    elif dxy[1] < 0:
        return left_right(dxy) + up_down(dxy) + ((0, 2),)
    else:
        return up_down(dxy) + left_right(dxy) + ((0, 2),)
