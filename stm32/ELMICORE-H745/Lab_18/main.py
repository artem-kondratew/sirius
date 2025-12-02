
from vpython import *
from time import *
import numpy as np
import math
import serial

# Открываем последовательный канал
ser = serial.Serial('com4', 115200)
sleep(1)

# Настраиваем сцену VPython
scene.range = 5
scene.background = color.yellow
toRad = 2 * np.pi / 360
toDeg = 1 / toRad
scene.forward = vector(-1, -1, -1)

scene.width = 1200
scene.height = 1080

# Вектора координатных осей VPython
xarrow = arrow(lenght=2, shaftwidth=.1, color=color.red, axis=vector(1, 0, 0))
yarrow = arrow(lenght=2, shaftwidth=.1, color=color.green, axis=vector(0, 1, 0))
zarrow = arrow(lenght=4, shaftwidth=.1, color=color.blue, axis=vector(0, 0, 1))

# Вектора осей датчика (платформы)
frontArrow = arrow(length=4, shaftwidth=.1, color=color.purple, axis=vector(1, 0, 0))
upArrow = arrow(length=1, shaftwidth=.1, color=color.magenta, axis=vector(0, 1, 0))
sideArrow = arrow(length=2, shaftwidth=.1, color=color.orange, axis=vector(0, 0, 1))

# Модель платформы
bBoard = box(length=2, width=3, height=.2, opacity=.8, pos=vector(0, 0, 0,))
myObj = bBoard

print('starting...')

while True:
    try:
        # Принимаем кватернионы по последовательному каналу
        while ser.inWaiting() == 0:
            pass
        dataPacket = ser.readline()
        dataPacket = str(dataPacket, 'utf-8')
        splitPacket = dataPacket.split(",")
        q0 = float(splitPacket[0])
        q1 = float(splitPacket[1])
        q2 = float(splitPacket[2])
        q3 = float(splitPacket[3])

        # Преобразуем кватернионы в углы Эйлера
        # https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
        roll = math.atan2(2 * (q0 * q1 + q2 * q3), 1 - 2 * (q1 * q1 + q2 * q2))
        pitch = math.asin(2 * (q0 * q2 - q3 * q1))
        yaw = math.atan2(2 * (q0 * q3 + q1 * q2), 1 - 2 * (q2 * q2 + q3 * q3))

        print(roll, pitch, yaw)

        # Ограничим частоту обновления изображения (50 Гц)
        rate(50)

        # Глобальная (неподвижная) система координат датчика, для которой получены углы
        # Эйлера, не совпадает с системой VPython.
        # Пусть k - фронтальный вектор платформы. Тогда координаты данного вектора при переходе
        # из глобальной системы координат датчика ICM-20948 в систему координат VPython 
        # описываются соотношениями:
        # Xk = Xk_icm; Yk = Zk_icm; Zk = -Yk_icm.
        # Зная, что 
        # Xk_icm = cos(yaw)*cos(pitch)
        # Yk_icm = sin(yaw)*cos(pitch)
        # Zk_icm = -sin(pitch)
        # получаем вектор k в системе координат VPython:
        k = vector(cos(yaw)*cos(pitch), -sin(pitch), -sin(yaw)*cos(pitch))
        # Для определения двух других векторов платформы (вертикального и бокового) воспользуемся
        # углом roll.
        # z - вспомогательный вертикальный вектор платформы:
        z = vector(0, 1, 0)
        # s - вспомогательный боковой вектор платформы:
        s = cross(z, k)
        # v - вертикальный вектор платформы до применения roll:
        v = cross(k, s)
        # vrot - вертикальный вектор платформы после roll по формуле Родригеса:
        # https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula
        vrot = v * cos(roll) + cross(k, v) * sin(roll)

        # Получаем вектора осей датчика в системе VPython
        frontArrow.axis = k
        sideArrow.axis = cross(vrot, k)
        upArrow.axis = vrot

        myObj.axis = k
        myObj.up = vrot

        sideArrow.length = 2
        frontArrow.length = 4
        upArrow.length = 1
    except KeyboardInterrupt:
        exit(0)
