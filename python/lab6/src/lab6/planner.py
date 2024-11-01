import cv2 as cv
import sys
import numpy as np

    
def load(image_path : str):
    return cv.imread(image_path, cv.IMREAD_GRAYSCALE)


def show(env):
    cv.imshow('map', env)
    if cv.waitKey(0) & 0xFF == ord('q'):
        return
    
    
def generate_path(env):
    rows, cols = env.shape[:2]
    
    w = np.zeros(env.shape, dtype=np.float64)
    w[0] = env[0]
    
    c = np.zeros((rows, cols, 2), dtype=np.float64)
    c[0] = np.array([(0, i) for i in range(cols)])
    
    for i in range(1, rows):
        w[i, 0] = 1 + np.float64(env[i, 0]) + w[i-1, 0]
        for j in range(1, cols):
            w[i, j] = np.float64(env[i, j])
            if w[i, j-1] < w[i-1, j]:
                if w[i, j-1] + 1 < w[i-1, j-1] + np.sqrt(2):
                    w[i, j] += w[i, j-1] + 1
                    c[i, j] = (i, j - 1)
                else:
                    w[i, j] += w[i-1, j-1] + np.sqrt(2)
                    c[i, j] = (i - 1, j - 1)
            else:
                if w[i-1, j] + 1 < w[i-1, j-1] + np.sqrt(2):
                    w[i, j] += w[i-1, j] + 1
                    c[i, j] = (i - 1, j)
                else:
                    w[i, j] += w[i-1, j-1] + np.sqrt(2)
                    c[i, j] = (i - 1, j - 1)
             
        for j in range(cols - 2, -1, -1):
            right_val = 1 + np.float64(env[i, j]) + w[i, j+1]
            diag_right_val = np.sqrt(2) + np.float64(env[i, j]) + w[i-1, j+1]
            if right_val < diag_right_val:
                if right_val < w[i, j]:
                    w[i, j] = right_val
                    c[i, j] = (i, j + 1)
            else:
                if diag_right_val < w[i, j]:
                    w[i, j] = diag_right_val
                    c[i, j] = (i - 1, j + 1)                
    
    # print(w)
    # print(c)
    
    idx = np.argmin(w, axis=1)[rows-1]
    
    path = [(rows - 1, int(idx))]
    idx = int(c[rows-1, idx][0]), int(c[rows-1, idx][1])
    
    while True:
        path.append(idx)
        idx = int(c[idx][0]), int(c[idx][1])
        print(idx)
        if idx[0] == 0:
            path.append(idx)
            break
    
    return path[::-1]
    
    
def draw(env, path):
    env = cv.cvtColor(env, cv.COLOR_GRAY2BGR)
    for pt in path:
        env[pt] = (0, 0, 255)
    return env


def draw_lines(env, path):
    env = cv.cvtColor(env, cv.COLOR_GRAY2BGR)
    for i in range(1, len(path)):
        cv.line(env, path[i-1][::-1], path[i][::-1], (0, 0, 255), 2)
    return env


def print_path(path):
    for pt in path:
        print(''.join(str(pt))[1:-1])


if __name__ == '__main__':
        
    env = np.array([[1, 3, 3, 4],
                    [7, 2, 6, 1],
                    [10, 9, 1, 2],
                    [4, 2, 5, 8],], dtype=np.uint8)
    
    # print(env)
    
    path = generate_path(env)
    print_path(path)
    
    print(path)
    
    env = draw(env, path)
    
    show(env)   
     