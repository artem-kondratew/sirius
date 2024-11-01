import sys
from lab1 import get_pi


if __name__ == '__main__':
    assert len(sys.argv) == 2 and int(sys.argv[1]) > 0, 'wrong input'

    digits = int(sys.argv[1])
    # t1 = time.time()
    pi = get_pi(digits)
    # t2 = time.time()
    print(pi)
    # print(len(pi))
    # print(t2 - t1)

