from lab5 import Transform2D, calculate_expr
from math import pi


if __name__ == '__main__':
    
    h = Transform2D(pi/4, [0, 0])

    pt1 = [1, 1]

    pt2 = h * pt1
    print(pt2)

    h2 = Transform2D(pi/4, [0, 0])

    h3 = h2 @ h
    print('h3:', h3)

    pt3 = [1, 0]
    pt4 = h3 * pt3
    print(pt4)

    print('inv')
    h = Transform2D(pi/4, [1, 2])
    h2 = h.inv
    print(h)
    print(h2)
    print(h @ h2)

    # CALCULATOR
    print('\nCALCULATOR\n')

    expr = 'rot(1.57) @ inv(tran(2, 3)) @ tran(2, 3) @ rot(-1.57/2) * [1, 0]'
    res = calculate_expr(expr)
    print(res)

    expr = 'rot(1.57) @ tran(3, 4)'
    res = calculate_expr(expr)
    print(res)

    expr = 'rot(1.57) @ tran(3, 4) * [1, 1]'
    res = calculate_expr(expr)
    print(res)
