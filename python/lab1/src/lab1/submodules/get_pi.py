import sys
from mpmath import mp, mpf, nstr
import time


def bbp(k : int):
    return mpf(16) ** -k * (mpf(4) / (8 * k + 1) - mpf(2) / (8 * k + 4) - mpf(1) / (8 * k + 5) - mpf(1) / (8 * k + 6))


def get_pi(digits : int) -> str:
    if digits == 1:
        return str(3)
    
    mp.dps = digits + 10

    pi = mpf(0)
    k = int((digits - 1) * mp.log(10) / mp.log(16)) + 1

    for i in range(k):
        pi += bbp(i)

    return nstr(pi, digits, strip_zeros=False)


if __name__ == '__main__':
    assert len(sys.argv) == 2 and int(sys.argv[1]) > 0, 'wrong input'

    digits = int(sys.argv[1])
    t1 = time.time()
    pi = get_pi(digits)
    t2 = time.time()
    print(pi)
    # print(len(pi))
    # print(t2 - t1)
