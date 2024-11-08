from numpy.polynomial import polynomial as P


p1 = [1.2, +1.5, 1.0]
p2 = [2, -2.1, 2]
p3 = [4, -5, 0, 2, 1, 4, 9]
p4 = [-3, 4, 8, 5, 3]
p5 = [0, 4, 6, 1, 7, 3, 2, 5]

result = P.polydiv(P.polysub(P.polymul(P.polyadd(p1, p2), p3), p4), p5)[1]

print(result)