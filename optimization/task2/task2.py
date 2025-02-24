import cv2 as cv
import cvxpy as cp
import matplotlib.pyplot as plt
import numpy as np
import os
import torch
import torch.nn as nn
import torch.optim as optim

from sklearn import svm

from dataloader import load_dataset


alpha = (0, np.pi / 4)
xc = (-2, 2)
yc = (1, -1)

size = 500

r = np.random.uniform(0, 1, size=size).reshape((size, 1))
phi = np.random.uniform(0, 2 * np.pi, size=size).reshape((size, 1))

use_task1 = False
use_task2 = False


def gen_x(k1, k2, alpha):
    def gen_x_(xc, yc, k1, k2, alpha):
        x = xc + k1 * r * np.cos(phi) * np.cos(alpha) - k2 * r * np.sin(phi) * np.sin(alpha)
        y = yc + k1 * r * np.cos(phi) * np.sin(alpha) + k2 * r * np.sin(phi) * np.cos(alpha)
        return np.hstack([x, y])
        
    x1 = gen_x_(xc[0], yc[0], k1[0], k2[0], alpha[0])
    x2 = gen_x_(xc[1], yc[1], k1[1], k2[1], alpha[1])
    return x1, x2, np.min([x1[:, 0], x2[:, 0]]), np.max([x1[:, 0], x2[:, 0]])


def draw_sets(x1, x2, line, sets_only=False):
    _, ax1 = plt.subplots(figsize=(8, 6))
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.grid(True)

    ax1.scatter(x1[:, 0], x1[:, 1], color='blue', label='set 1')
    ax1.scatter(x2[:, 0], x2[:, 1], color='red', label='set 2')
    if not sets_only:
        ax1.plot(line[0], line[1], color='black', label='line')

    ax1.legend(loc='upper left')


def calc_line_coeffs(x1, x2, use_norm):
    print(x1.shape)
    u = cp.Variable((size, 1))
    v = cp.Variable((size, 1))
    a = cp.Variable((2, 1))
    b = cp.Variable((1, 1))
    constraints = [
        a.T @ x1.T + b >= 1 - u,
        a.T @ x2.T + b <= -1 + v,
        u >= 0,
        v >= 0,
    ]
    if use_norm:
        objective = cp.Minimize(0.0001 * cp.norm2(a) + 1 * (cp.sum(u) + cp.sum(v)))
    else:
        objective = cp.Minimize(cp.sum(u) + cp.sum(v))
    problem = cp.Problem(objective, constraints)
    problem.solve(verbose=True, solver=cp.ECOS)
    return a.value, b.value


def get_line(x_min, x_max, a, b):
    def line(x):
        return 1 / a[1][0] * (-a[0][0] * x - b[0])
    x_line = [x_min, x_max]
    y_line = [line(x_min), line(x_max)]
    return (x_line, y_line)


def task1():
    global use_task1
    use_task1 = True

    k1 = (3, 4)
    k2 = (1, 1)

    x1, x2, x_min, x_max = gen_x(k1, k2, alpha)

    a, b = calc_line_coeffs(x1, x2, True)
    line1 = get_line(x_min, x_max, a, b)

    a, b = calc_line_coeffs(x1, x2, False)
    line2 = get_line(x_min, x_max, a, b)
    
    draw_sets(x1, x2, line1)
    draw_sets(x1, x2, line2)

    print(x1.shape)


def task2():
    global use_task2
    use_task2 = True

    k1 = (3, 4)
    k2 = (2.5, 2)

    x1, x2, x_min, x_max = gen_x(k1, k2, alpha)

    # scikit-learn

    clf = svm.SVC(kernel='linear')

    X = np.vstack([x1, x2])
    y = np.array([1] * x1.shape[0] + [2] * x2.shape[0])

    clf.fit(X, y)

    a = clf.coef_.T
    b = clf.intercept_

    print(a, b)

    line1 = get_line(x_min, x_max, a, b)

    draw_sets(x1, x2, line1)

    # torch

    X = torch.tensor(np.vstack([x1, x2]), dtype=torch.float32)
    y = torch.tensor(np.array([1] * x1.shape[0] + [-1] * x2.shape[0]), dtype=torch.float32).view(-1, 1)

    class SVM_Network(nn.Module):
        def __init__(self):
            super(SVM_Network, self).__init__()
            self.fc1 = nn.Linear(2, 1)

        def forward(self, x):
            return self.fc1(x)

    model = SVM_Network()
    optimizer = optim.SGD(model.parameters(), lr=0.01)

    epochs = 5000
    for epoch in range(epochs):
        model.train()

        optimizer.zero_grad()

        outputs = model(X)

        u = torch.relu(1 - y * outputs)  # Для класса 1: условие 1 - y * output >= 0
        v = torch.relu(1 + y * outputs)  # Для класса 2: условие 1 + y * output <= 0

        loss = torch.norm(model.fc1.weight) + torch.sum(u) + torch.sum(v)

        loss.backward()
        optimizer.step()

        if epoch % 100 == 0:
            print(f'Epoch {epoch}, Loss: {loss.item()}')

    model.eval()

    a = model.fc1.weight.detach().numpy().T
    b = model.fc1.bias.detach().numpy()

    print(a, b)

    line = get_line(x_min, x_max, a, b)

    draw_sets(x1, x2, line)


def task3():
    path = os.path.join(os.path.pardir, 'dataset')
    images_train, labels_train, images_test, labels_test = load_dataset(path)

    train_list = []
    test_list = []

    train_size = 100
    test_size = 980

    w = images_train[0].shape[0]

    label1 = 0
    label2 = 1

    for label in (label1, label2):
        train = images_train[labels_train==label]
        train = np.reshape(train[:train_size], (train_size, w ** 2)).T
        train_list.append(train)

        test_images_i = images_test[labels_test==label]
        test_images_i = np.reshape(test_images_i[:test_size], (test_size, w ** 2)).T
        test_list.append(test_images_i)

    images_train = np.array(train_list, dtype=object)
    images_test = np.array(test_list, dtype=object)

    u = cp.Variable((images_train[0].shape[1], 1))
    v = cp.Variable((images_train[0].shape[1], 1))
    a = cp.Variable((images_train[0].shape[0], 1))
    b = cp.Variable((1, 1))

    constraints = [
        a.T @ images_train[0] + b >= 1 - u,
        a.T @ images_train[1] + b <= -1 + v,
        u >= 0,
        v >= 0,
    ]

    objective = cp.Minimize(cp.norm2(a) + cp.sum(u) + cp.sum(v))

    problem = cp.Problem(objective, constraints)
    # problem.solve(verbose=True)

    # a = a.value
    # b = b.value

    # a.tofile('a.data')
    # b.tofile('b.data')

    a = np.fromfile('a.data', dtype=np.float64)
    b = np.fromfile('b.data', dtype=np.float64)

    print(images_train.shape)

    # cv.imwrite('0.png', images_train[0].T[0].astype(np.uint8).reshape((w, w)))
    # cv.imwrite('1.png', images_train[1].T[0].astype(np.uint8).reshape((w, w)))
    # cv.waitKey(0)

    fails_zero = 0
    fails_ones = 0
    fails_zero_list = []
    fails_ones_list = []
    for i in range(test_size):
        if a.T @ images_test[0].T[i] + b < 0:
            fails_zero += 1
            fails_zero_list.append(images_test[0].T[i].astype(np.uint8).reshape((w, w)))
        if a.T @ images_test[1].T[i] + b > 0:
            fails_ones += 1
            fails_ones_list.append(images_test[1].T[i].astype(np.uint8).reshape((w, w)))

    print(fails_zero, fails_ones)

    print('zeros fails:', fails_zero / test_size)

    i = 0
    for img in fails_zero_list:
        cv.imshow('zeros fails', img)
        # cv.imwrite(f'fail{i}.png', img)
        i+= 1
        cv.waitKey(0)

    print('ones fails:', fails_ones / test_size)

    for img in fails_ones_list:
        cv.imshow('ones fails', img)
        cv.waitKey(0)

    # zero = images_test[0][15]
    # one = images_test[1][15]

    # print(a.T @ zero + b > 0, a.T @ one + b < 0)


if __name__ == '__main__':
    # task1()
    # task2()
    task3()

    if use_task1 or use_task2:
        plt.tight_layout()
        plt.show()
