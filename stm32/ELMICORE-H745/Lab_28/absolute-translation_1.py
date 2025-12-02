import sensor
import time

from pyb import Servo

from pid import PID


sensor.reset()  # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)  # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.B64X64)  # Set frame size to 64x64... (or 64x32)...
sensor.skip_frames(time=2000)  # Wait for settings take effect.
clock = time.clock()  # Create a clock object to track the FPS.

# Take from the main frame buffer's RAM to allocate a second frame buffer.
# There's a lot more RAM in the frame buffer than in the MicroPython heap.
# However, after doing this you have a lot less RAM for some algorithms...
# So, be aware that it's a lot easier to get out of RAM issues now.
extra_fb = sensor.alloc_extra_fb(sensor.width(), sensor.height(), sensor.RGB565)
extra_fb.replace(sensor.snapshot())


yaw_servo=Servo(1)
pitch_servo=Servo(2)

yaw_servo.calibration(500,2500,500)
pitch_servo.calibration(500,2500,500)

yaw_min = -90
yaw_max = 90
pitch_min = -45
pitch_max = 70

wait_ms = 2000


def set_yaw(angle):
    angle = max(yaw_min, angle)
    angle = min(yaw_max, angle)
    yaw_servo.angle(90 + angle)

def set_pitch(angle):
    angle = max(pitch_min, angle)
    angle = min(pitch_max, angle)
    pitch_servo.angle(75 - angle)


set_yaw(0)
set_pitch(0)

pid_x = PID(0.1, 0.1, 0, 20)
pid_y = PID(0.1, 0.1, 0, 20)

yaw = 0
pitch = 0

sensor.skip_frames(time = wait_ms*2)

time.sleep(4)

while True:
    clock.tick()  # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot()  # Take a picture and return the image.

    # For this example we never update the old image to measure absolute change.
    displacement = extra_fb.find_displacement(img)

    cx, cy = int(img.width() / 2), int(img.height() / 2)

    # Offset results are noisy without filtering so we drop some accuracy.
    sub_pixel_x = int(displacement.x_translation() * 5) / 5.0
    sub_pixel_y = int(displacement.y_translation() * 5) / 5.0

    if (
        displacement.response() > 0.1
    ):  # Below 0.1 or so (YMMV) and the results are just noise.
        print(
            "{0:+f}x {1:+f}y {2} {3} FPS".format(
                sub_pixel_x, sub_pixel_y, displacement.response(), clock.fps()
            )
        )
        img.draw_cross(cx, cy, color=(0, 255, 0))
        cx_old, cy_old = int(cx - sub_pixel_x), int(cy + sub_pixel_y)
        img.draw_cross(cx_old, cy_old, color=(255, 0, 255))

        ux = pid_x.get_pid(sub_pixel_x, 1)
        uy = pid_y.get_pid(sub_pixel_y, 1)

        yaw -= ux
        pitch += uy

        set_yaw(yaw)
        set_pitch(pitch)

    else:
        print(clock.fps())

    print(img.compressed_for_ide(), end='')
