from vpython import *
from time import *
import numpy as np
import math
import serial

# ---------- AlphaFilter ----------
class AlphaFilter:
    def __init__(self, arr, alpha):
        self.arr = arr
        self.alpha = alpha

    def spin(self, arr):
        new_arr = self.alpha * self.arr + (1 - self.alpha) * arr
        self.arr = new_arr
        return new_arr

# ---------- Функция устранения флипа ----------
def unwrap_angle(prev, new):
    diff = new - prev
    if diff > np.pi:
        new -= 2*np.pi
    elif diff < -np.pi:
        new += 2*np.pi
    return new

# ---------- Rotation matrices ----------
def Rx(a):
    ca = np.cos(a); sa = np.sin(a)
    return np.array([[1, 0, 0],
                     [0, ca, -sa],
                     [0, sa, ca]])

def Ry(a):
    ca = np.cos(a); sa = np.sin(a)
    return np.array([[ca, 0, sa],
                     [0, 1, 0],
                     [-sa, 0, ca]])

def Rz(a):
    ca = np.cos(a); sa = np.sin(a)
    return np.array([[ca, -sa, 0],
                     [sa,  ca, 0],
                     [0,   0,  1]])

# ---------- Serial ----------
ser = serial.Serial('com10', 115200)
sleep(1)

# ---------- VPython Scene ----------
scene.range = 5
scene.background = color.yellow
scene.forward = vector(-1, -1, -1)
scene.width = 1200
scene.height = 1080

# Оси VPython
xarrow = arrow(length=2, shaftwidth=.1, color=color.red,   axis=vector(1, 0, 0))
yarrow = arrow(length=2, shaftwidth=.1, color=color.green, axis=vector(0, 1, 0))
zarrow = arrow(length=4, shaftwidth=.1, color=color.blue,  axis=vector(0, 0, 1))

# Платформа
frontArrow = arrow(length=4, shaftwidth=.1, color=color.purple,  axis=vector(1, 0, 0))
upArrow    = arrow(length=1, shaftwidth=.1, color=color.magenta, axis=vector(0, 1, 0))
sideArrow  = arrow(length=2, shaftwidth=.1, color=color.orange,  axis=vector(0, 0, 1))

bBoard = box(length=2, width=3, height=.2, opacity=.8, pos=vector(0, 0, 0))
myObj = bBoard

# ---------- AlphaFilter ----------
alpha_filter = AlphaFilter(np.zeros(6), 0.97)

# ======================= MAIN LOOP =======================
while True:
    try:
        while ser.inWaiting() == 0:
            pass

        dataPacket = ser.readline().decode('utf-8').strip()
        splitPacket = dataPacket.split(",")

        # ----- raw data -----
        tx = float(splitPacket[0])
        ty = float(splitPacket[1])
        tz = float(splitPacket[2])

        roll  = float(splitPacket[3]) * np.pi / 180.0
        pitch = float(splitPacket[4]) * np.pi / 180.0
        yaw   = float(splitPacket[5]) * np.pi / 180.0

        # Нормализация углов к (-pi, pi)
        roll  = np.atan2(np.sin(roll),  np.cos(roll))
        pitch = np.atan2(np.sin(pitch), np.cos(pitch))
        yaw   = np.atan2(np.sin(yaw),   np.cos(yaw))

        # ---------- Устранение флипов через AlphaFilter.arr ----------
        roll  = unwrap_angle(alpha_filter.arr[3], roll)
        pitch = unwrap_angle(alpha_filter.arr[4], pitch)
        yaw   = unwrap_angle(alpha_filter.arr[5], yaw)

        # Ограничим частоту обновления изображения (50 Гц)
        rate(50)

        rx = Rx(roll)
        ry = Ry(pitch)
        rz = Rz(-yaw)

        r = rx @ ry @ rz

        k = r[:, 0]
        k = vector(k[0], k[1], k[2])

        t = np.round(np.array([tx, ty, tz]), 2)
        tvx, tvy, tvz = t[2], t[0], -t[1]
        print(-tvx, tvy, tvz)

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
