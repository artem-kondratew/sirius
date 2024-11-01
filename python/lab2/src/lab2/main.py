import sys
import time
from copy import deepcopy


def draw_state(state : list) -> str:
    out = ''
    for row in state:
        for symbol in row:
            print('*' if symbol else ' ', end='')
            out += '*' if symbol else ' '
        print()
        out += '\n'
    print('\n')
    out += '\n'
    
    return out


def is_row_full(row : list) -> bool:
    return ' ' not in row


def proc(data : list) -> list:
    state = deepcopy(data)
    
    for i in range(len(state) - 2, -1, -1):
        for j in range(len(state[0])):
            
            if state[i][j] != 1:
                continue

            if j == 0:
                if state[i+1][j] == 0:
                    state[i+1][j] = 1
                    state[i][j] = 0
                    continue
                
                if state[i+1][j] == 1 and state[i+1][j+1] == 0:
                    state[i+1][j+1] = 1
                    state[i][j] = 0
                    
                continue
            
            elif j == (len(state[0]) - 1):
                if state[i+1][j] == 0:
                    state[i+1][j] = 1
                    state[i][j] = 0
                    continue
                    
                if state[i+1][j] == 1 and state[i+1][j-1] == 0:
                    state[i+1][j-1] = 1
                    state[i][j] = 0
                    
                continue
            
            else:
                if state[i+1][j] == 0:
                    state[i+1][j] = 1
                    state[i][j] = 0
                    continue
                    
                if state[i+1][j] == 1 and state[i+1][j-1] == 0 and state[i+1][j+1] == 0:
                    if (i + j) % 2 == 0:
                        state[i+1][j-1] = 1
                        state[i][j] = 0
                    else:
                        state[i+1][j+1] = 1
                        state[i][j] = 0
                    continue
                        
                if state[i+1][j] == 1 and state[i+1][j-1] == 0 and state[i+1][j+1] == 1:
                    state[i+1][j-1] = 1
                    state[i][j] = 0
                    continue
                    
                if state[i+1][j] == 1 and state[i+1][j-1] == 1 and state[i+1][j+1] == 0:
                    state[i+1][j+1] = 1
                    state[i][j] = 0
                    continue
                
    return state


def main():
    assert len(sys.argv) == 2, 'wrong input'
    
    s = '*'

    with open(sys.argv[1], 'r') as file:
        strings = file.read().split('\n')
        data = [[1 if symbol == s else 0 for symbol in string] for string in strings]
    
    out = draw_state(data)

    while True:
        new_data = proc(data)
        if new_data == data:
            break
        out += draw_state(new_data)
        data = new_data
        # time.sleep(0.5)
        
    return out
    
    
if __name__ == '__main__':
    main()
