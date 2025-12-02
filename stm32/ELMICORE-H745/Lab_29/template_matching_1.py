# This work is licensed under the MIT license.
# Copyright (c) 2013-2023 OpenMV LLC. All rights reserved.
# https://github.com/openmv/openmv/blob/master/LICENSE
#
# Template Matching Example - Normalized Cross Correlation (NCC)
#
# This example shows off how to use the NCC feature of your OpenMV Cam to match
# image patches to parts of an image... expect for extremely controlled environments
# NCC is not all to useful.
#
# WARNING: NCC supports needs to be reworked! As of right now this feature needs
# a lot of work to be made into somethin useful. This script will remain to show
# that the functionality exists, but, in its current state is inadequate.

import time
import sensor
import image
from image import SEARCH_EX
from pyb import UART, Servo
from pid import PID

uart = UART(3, 115200)

yaw_servo=Servo(1)
pitch_servo=Servo(2)

yaw_servo.calibration(500,2500,500)
pitch_servo.calibration(500,2500,500)

yaw_min = -90
yaw_max = 90
pitch_min = -45
pitch_max = 70


def set_yaw(angle):
    angle = max(yaw_min, angle)
    angle = min(yaw_max, angle)
    yaw_servo.angle(90 + angle)

def set_pitch(angle):
    angle = max(pitch_min, angle)
    angle = min(pitch_max, angle)
    pitch_servo.angle(75 - angle)


pid_x = PID(0.05, 0.01, 0, 2)
pid_y = PID(0.05, 0.01, 0, 2)

yaw = 0
pitch = -10

template_matching = False

# Reset sensor
sensor.reset()
sensor.set_vflip(True)
sensor.set_hmirror(True)

# Set sensor settings
if template_matching:
    sensor.set_contrast(1)
    sensor.set_framesize(sensor.QQVGA)
    sensor.set_windowing((64, 64))
else:
    sensor.set_contrast(3)
    sensor.set_framesize(sensor.VGA)
    sensor.set_auto_gain(False, gain_db=1)
    sensor.set_windowing((320, 240))

sensor.set_gainceiling(16)
sensor.set_pixformat(sensor.GRAYSCALE)

clock = time.clock()

set_yaw(yaw)
set_pitch(pitch)

sensor.skip_frames(time=2000)


def find_target():
    global yaw, pitch
    while True:
        clock.tick()
        img = sensor.snapshot()

        print(img.compressed_for_ide(), end='')

        if uart.any() < 3:
            continue

        data = [d for d in uart.read(3)]

        assert data[0] < 2, data

        print(data)

        if data[0] == 1:
            return img.copy()

        data[1] -= 100
        data[2] -= 100

        if abs(data[1]) > 20:
            direction = 1 if data[1] > 0 else -1
            yaw += direction
            set_yaw(yaw)

        if abs(data[2]) > 20:
            direction = -1 if data[2] > 0 else 1
            pitch += direction
            set_pitch(pitch)


if template_matching:
    template = find_target()
    sensor.set_windowing((160, 120))
else:
    source = find_target()
    rect_list = [160-64, 120-64, 128, 128]
    kpts1 = source.find_keypoints(max_keypoints=150, threshold=10, scale_factor=1.2, roi=rect_list)


if template_matching:
    cx, cy = 80, 60
else:
    cx, cy = 160, 120

while True:
    clock.tick()
    img = sensor.snapshot()

    if template_matching:
        r = img.find_template(
            template, 0.70, step=4, search=SEARCH_EX
        )  # , roi=(10, 0, 60, 60))
    else:
        r = None
        kpts2 = img.find_keypoints(max_keypoints=150, threshold=10, normalized=True)
        if kpts2:
            match = image.match_descriptor(kpts1, kpts2, threshold=85)
            if match.count() > 10:
                r = match.rect()
                # If we have at least n "good matches"
                # Draw bounding rectangle and cross.
                img.draw_rectangle(match.rect())
                img.draw_cross(match.cx(), match.cy(), size=10)

#            print(kpts2, "matched:%d dt:%d" % (match.count(), match.theta()))
        print(kpts1)

    if r is not None:
        img.draw_rectangle(r)

        cx_new = r[0] + r[2]/2
        cy_new = r[1] + r[3]/2

        ux = pid_x.get_pid(cx - cx_new, 1)
        uy = pid_y.get_pid(cy - cy_new, 1)

        yaw += ux
        pitch += uy

        set_yaw(yaw)
        set_pitch(pitch)

    print(clock.fps())
    print(img.compressed_for_ide(), end='')
