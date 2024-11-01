from math import sin, cos
import sys
import numpy as np


class Transform2D:
    
    def __init__(self, rot : float, tran : list):
        self.rot = rot
        self.tran = tran
        
    def __str__(self) -> str:
        return f'rot = {round(self.rot, 4)}; tran = ({round(self.tran[0], 4)}, {round(self.tran[1], 4)})'
    
    def __mul__(self, pt):
        x = cos(self.rot) * pt[0] - sin(self.rot) * pt[1] + self.tran[0]
        y = sin(self.rot) * pt[0] + cos(self.rot) * pt[1] + self.tran[1]
        return [np.float64(round(x, 4)), np.float64(round(y, 4))]
    
    def __matmul__(self, other):
        rot = self.rot + other.rot
        x = cos(self.rot) * other.tran[0] - sin(self.rot) * other.tran[1] + self.tran[0]
        y = sin(self.rot) * other.tran[0] + cos(self.rot) * other.tran[1] + self.tran[1]
        return Transform2D(rot, [x, y])
    
    @property
    def inv(self):
        rot = -self.rot
        x = -(cos(rot) * self.tran[0] - sin(rot) * self.tran[1])
        y = -(sin(rot) * self.tran[0] + cos(rot) * self.tran[1])
        return Transform2D(rot, [x, y])
    

def tran(tx : float, ty : float):
    return Transform2D(0, [tx, ty])


def rot(rot : float):
    return Transform2D(rot, [0, 0])


def inv(tf : Transform2D):
    return tf.inv


def calculate_expr(expr : str):
    idx = 0
    for i, s in enumerate(expr):
        if s == '@':
            idx = i
    if expr[-1] == ']':
        expr = expr[:idx] + '*' + expr[idx+1:]
    return eval(expr)

if __name__ == '__main__':
    assert len(sys.argv) == 2, 'wrong input'
    print(calculate_expr(sys.argv[1]))
