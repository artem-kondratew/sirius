# sim params
t1 = 100.0
dt = 0.0001

# system params
k1 = 0.5
k2 = 0.5
c1 = 0.012195
c2 = 0.00272
J1 = 0.29462
J2 = 0.292045

# birth month $ day
m = 9
d = 1

a21 = -k1 / J1
a22 = -c1 / J1
a23 = k1 / J1
a41 = k1 / J2
a43 = -(k1 + k2) / J2
a44 = -c2 / J2

b = 1 / J1

# Lipschitz constants for cont.
# and disc. controllers
Lc = 50
Ld = 10