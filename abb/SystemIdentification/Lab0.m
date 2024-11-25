p = 1;
q = 0;
r = 0;
w = 9;

a = 1 / (p + q);
b = r + w;
c = p + q + r + w;

s = tf('s');

model = tf(1, [1, a * b, a * c])

bode(model)