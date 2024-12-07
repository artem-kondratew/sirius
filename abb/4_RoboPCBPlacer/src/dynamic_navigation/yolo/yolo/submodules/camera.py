from .Data import Data, Component, Board
import numpy as np
import cv2 as cv
import numpy as np
from scipy.spatial.transform import Rotation as R
import cv2.aruco as aruco
import math


# def get_data(frame):
#     c0 = Component(0, [0, 2, 3], [1, 2, 3, 4])
#     c1 = Component(1, [1, 2, 3], [1, 2, 3, 4])
#     c2 = Component(2, [2, 2, 3], [1, 2, 3, 4])
#     c3 = Component(3, [3, 2, 3], [0, 8, 9, 5])
#     c4 = Component(4, [4, 2, 3], [1, 3, 6, 8])
#     c5 = Component(5, [5, 2, 3], [1, 3, 6, 8])

#     board = Board(2, [3, 4, 5], [0, 0, 0, 0])

#     data = Data([c0, c1, c2, c3, c4], board)

#     return data


mtx = np.array([[612.64599609375, 0, 327.8221130371094],
                [0, 611.58642578125, 234.41448974609375],
                [0, 0, 1]])

aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()

h, w = 480, 640


def coords_cam_to_real(x_cam, y_cam):  

    fx, fy = mtx[0, 0], mtx[1, 1]
    cx, cy = mtx[0, 2], mtx[1, 2]

    Z_plane = 0.852

    X_c = (x_cam - cx) * Z_plane / fx + 0.01
    Y_c = -((y_cam - cy) * Z_plane / fy - 0.01)

    return X_c, Y_c


def rotate_quaternion_180_x(q):
    # Кватернион для поворота на 180 градусов вокруг X
    q_rot = [0, 1, 0, 0]

    # Распакуем входной кватернион
    w1, x1, y1, z1 = q
    w2, x2, y2, z2 = q_rot

    # Умножение кватернионов
    w_res = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x_res = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y_res = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
    z_res = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2

    return [w_res, x_res, y_res, z_res]


def rotate_quaternion_90_z(q):
    # Кватернион для поворота на 180 градусов вокруг X
    sqrt2_over_2 = math.sqrt(2) / 2
    q_rot = (sqrt2_over_2, 0, 0, sqrt2_over_2)

    # Распакуем входной кватернион
    w1, x1, y1, z1 = q
    w2, x2, y2, z2 = q_rot

    # Умножение кватернионов
    w_res = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x_res = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y_res = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
    z_res = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2

    return [w_res, x_res, y_res, z_res]


def points_to_quaternion(v1_point, v2_point, center_point, use_useless : bool):
    v1_point = np.array(v1_point)
    v2_point = np.array(v2_point)
    center_point = np.array(center_point)

    vector_1 = np.subtract(v1_point, center_point)
    vector_2 = np.subtract(v2_point, center_point)

    v1 = np.array((vector_1[0], vector_1[1], 0))
    v2 = np.array((vector_2[0], vector_2[1], 0))

    # Нормализация векторов
    v1 = v1 / np.linalg.norm(v1)
    v2 = v2 / np.linalg.norm(v2)

    # Создание ортонормального базиса
    x = v1
    z = np.cross(v1, v2)
    z = z / np.linalg.norm(z)
    y = np.cross(z, x)

    # z[2] = -z[2]

    # Матрица вращения
    R_matrix = np.array([x, y, z]).T

    # Преобразование в кватернион
    rotation = R.from_matrix(R_matrix)
    quaternion = rotation.as_quat()  # (x, y, z, w)

    q = quaternion
    q = [q[3], q[0], q[1], -q[2]]
    
    return rotate_quaternion_90_z(rotate_quaternion_180_x(q)) if use_useless else q


def quaternion_to_vector(quaternion, image, c : tuple):
    rotation = R.from_quat(quaternion)
    direction_vector = rotation.apply([0, 0, 1])  # Применяем к оси Z

    scale = 30000

    end_point = (
        int(c[0] + direction_vector[0] * scale),
        int(c[1] - direction_vector[1] * scale)  # Инвертируем Y для OpenCV
    )

    cv.line(image, (c[0]+50, c[1]), end_point, (255, 0, 0), 1)

    return image


def get_data(frame, logger):

    h, w = frame.shape[:2]

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    components = []
    board = None

    corners, ids, rejected = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    if ids is None or len(ids) == 0:
        logger.info('ids is None')
        return None
    else:
        logger.info(f'ids: {ids}')
    flag = False
    for i in range(len(corners)):

        if int(ids[i]) <= 2:
            flag = True

        if int(ids[i]) > 2:
            
            l = (6, 7)
            if int(ids[i]) not in (l):
                translated_id = int(ids[i])- 3
            else:
                translated_id = 5 if int(ids[i]) == 7 else 4

            points = corners[i]  # Формат: [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
            x = (points[0][0][0] + points[0][1][0] + points[0][2][0] + points[0][3][0]) / 4
            y = (points[0][0][1] + points[0][1][1] + points[0][2][1] + points[0][3][1]) / 4
            center_of_component = np.mean(points, axis=0)  # Среднее значение по осям x и y

            logger.info(f'check center: {points}\n{center_of_component}\n{(x, y)}')

            components.append(Component(translated_id, coords_cam_to_real(x, y), points_to_quaternion(
                corners[i][0][1],  # Точка 1
                corners[i][0][3],  # Точка 2
                corners[i][0][0],   # Точка 3
                True
            ))) 
        else:
            quaternion = points_to_quaternion(
                corners[i][0][1],  # Точка 1
                corners[i][0][3],  # Точка 2
                corners[i][0][0],   # Точка 3
                False
            )
            ids_conv = {
                0 : 2,
                1 : 1,
                2 : 0
            }

            center_pix = int(corners[i][0][0][0]), int(corners[i][0][0][1])
            center = coords_cam_to_real(corners[i][0][0][0], corners[i][0][0][1])
            board = Board(ids_conv[int(ids[i])], center, quaternion)
     
    data = Data(components, board)

    # frame = quaternion_to_vector(quaternion, frame, center_pix)

    cv.line(frame, (int(w/2), int(h/2)), (int(w/2), 0), (255, 0, 0), 1)
    cv.line(frame, (int(w/2), int(h/2)), (int(w), int(h/2)), (255, 0, 0), 1)

    cv.destroyAllWindows()
    aruco.drawDetectedMarkers(frame, corners, ids)
    cv.imshow('frame', frame)
    cv.waitKey(1)

    logger.info(f'{data}')

    for i, marker_id in enumerate(ids):
        print(f"Маркер ID of board: {marker_id[0]}, Углы: {corners[i]}")

    frame = None

    return data
