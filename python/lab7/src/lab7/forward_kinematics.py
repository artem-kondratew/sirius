import sys
from dataclasses import dataclass
import numpy as np
import json
from casadi import SX, Function, jacobian, vertcat

# "[0.15, 0.20]" "[0.10, 0.30]"
@dataclass
class Data:
    links : np.ndarray


class Manipulator:
    
    def __init__(self, filepath : str):
        with open(filepath, 'r') as file:
            js = json.load(file)
            self.links = list(Data(**js).links)
            
        self.n = len(self.links)
        
        # print(f'links = {self.links}')
        
    def get_xyt(self, qi : list, dqi : list):
        if len(self.links) != len(qi) or len(self.links) != len(dqi):
            print('wrong input size')
            exit(0)
        
        # print(f'q = {qi}')
        # print(f'dq = {dqi}')
        
        x = 0
        y = 0
        t = 0
        
        q = SX.sym('q', self.n, 1)
        dq = SX.sym('dq', self.n, 1)
        
        for i in range(self.n):
            t += q[i]
            x += self.links[i] * SX.cos(t)
            y += self.links[i] * SX.sin(t)
            
        X = vertcat(x, y, t)
        V = jacobian(X, q) @ dq
        
        fX = Function('fX', [q, dq], [X])
        fV = Function('fdX', [q, dq], [V])
        
        # print(X)
        # print(V)
        
        Xi, Vi = fX(qi, dqi), fV(qi, dqi)
        
        # print(f'X = {Xi}', f'V = {Vi}', sep='\n')
        
        print(f'pose: {round(float(Xi[0]), 4)}, {round(float(Xi[1]), 4)}, {round(float(Xi[2]), 4)}')
        print(f'velocity: {round(float(Vi[0]), 4)}, {round(float(Vi[1]), 4)}, {round(float(Vi[2]), 4)}')
        
        return Xi, Vi
        
        
if __name__ == '__main__':
    assert len(sys.argv) == 4, 'wrong input'
    
    filepath = sys.argv[1]
    q = eval(sys.argv[2])
    dq = eval(sys.argv[3])
    
    manipulator = Manipulator(filepath)
    
    manipulator.get_xyt(q, dq)
