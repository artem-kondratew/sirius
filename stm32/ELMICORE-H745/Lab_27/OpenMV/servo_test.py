import sensor, image, time, gc

from pyb import Servo, delay, LED, UART

uart = UART(3, 4_000_000)

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # use RGB565.
sensor.set_framesize(sensor.QVGA) # use QQVGA for speed.
sensor.set_auto_whitebal(False) # turn this off.
sensor.skip_frames(10) # Let new settings take affect.

clock = time.clock() # Tracks FPS.

def send_array(arr, w, h):
    sz = w * h
    bucket = int(sz / 5.)
    uart.write(arr[:bucket])
    uart.write(arr[bucket:bucket*2])
    uart.write(arr[bucket*2:bucket*3])
    uart.write(arr[bucket*3:bucket*4])
    uart.write(arr[bucket*4:])

def send_img(img : image.Image):
    w, h = img.width(), img.height()
    arr = img.bytearray()
    yellow = 0xFFE0
    arr[4] = (yellow >> 8) & 0xFF
    arr[5] = yellow & 0xFF
    send_array(arr, w, h)

def sign_fun(x):
    if abs(x) < 10e-6:
       return 0
    return x / abs(x)

#def send_frame_over_uart(img):
#    # Сжимаем кадр
#    jpeg = img.compress(quality=90)
#    size = len(jpeg)

#    # Простой заголовок: 0xAA 0x55 + 2 байта длины
#    header = bytearray(4)
#    header[0] = 0xAA
#    header[1] = 0x55
#    header[2] = (size >> 8) & 0xFF
#    header[3] = size & 0xFF

#    uart.write(header)
#    uart.write(jpeg)

TRIGGER_THRESHOLD = 5
MOTION_THRESHOLD  = 60
DEG_PER_PIXEL_X = 0.2
DEG_PER_PIXEL_Y = 0.2
sensor.reset()  # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565)  # or sensor.GRAYSCALE
sensor.set_framesize(sensor.QVGA)  # or sensor.QQVGA (or others)
sensor.skip_frames(time=2000)  # Let new settings take affect.
sensor.set_auto_whitebal(False)  # Turn off white balance.
sensor.set_vflip(True)
sensor.set_hmirror(True)
clock = time.clock()  # Tracks FPS.
target_locked = False

pan_servo=Servo(1)
tilt_servo=Servo(2)
pan_servo.calibration(500,2500,500)
tilt_servo.calibration(500,2500,500)
wait_ms = 2000
pan_angle_min = -70
pan_angle_max = 70
tilt_angle_min = -65
tilt_angle_max = 35
pan_angle = 0
tilt_angle = 0
sign = 1

direction = 1 # Tower Pro SG90: -1, Fitec FS90MG: 1

# Move to center

curr_pan = 90
curr_tilt = 90
pan_servo.angle(90 - direction * pan_angle, wait_ms)
tilt_servo.angle(90 + direction * tilt_angle, wait_ms)
sensor.skip_frames(time = wait_ms)

# Take from the main frame buffer's RAM to allocate a second frame buffer.
# There's a lot more RAM in the frame buffer than in the MicroPython heap.
# However, after doing this you have a lot less RAM for some algorithms...
# So, be aware that it's a lot easier to get out of RAM issues now. However,
# frame differencing doesn't use a lot of the extra space in the frame buffer.
# But, things like AprilTags do and won't work if you do this...
extra_fb = sensor.alloc_extra_fb(sensor.width(), sensor.height(), sensor.RGB565)

print("About to save background image...")
sensor.skip_frames(time=2000)  # Give the user time to get ready.
extra_fb.replace(sensor.snapshot())
print("Saved background image - Now frame differencing!")
sensor.skip_frames(time=5000)

while True:
    clock.tick()

    img = sensor.snapshot()#.to_grayscale()

    img_cx = img.width() // 2
    img_cy = img.height() // 2

    if not target_locked:
        cx = img_cx
        cy = img_cy
        img.difference(extra_fb)

        diff = img.to_grayscale(copy=True)
        diff.binary([(MOTION_THRESHOLD, 255)])

        blobs = diff.find_blobs(
            [(200, 255)],
            pixels_threshold=50,
            area_threshold=50,
            merge=True
        )

        if blobs:
            largest_blob = max(blobs, key=lambda b: b.pixels())
            cx = largest_blob.cx()
            cy = largest_blob.cy()
            img.draw_rectangle(largest_blob.rect(), color=(255, 0, 0))
            img.draw_cross(cx, cy, color=(255, 0, 0))

        img.draw_cross(img_cx, img_cy, color=(255, 255, 255))
        print(img.compressed_for_ide(), end='')

        diff_x = img_cx - cx
        diff_y = img_cy - cy
        delta_pan  = DEG_PER_PIXEL_X * diff_x
        delta_tilt = DEG_PER_PIXEL_Y * diff_y
        dir_x = sign_fun(diff_x)
        dir_y = sign_fun(diff_y)
        print(diff_x, diff_y)
        print(dir_x, dir_y)

        curr_pan += dir_x * abs(delta_pan)
        curr_tilt -= dir_y * delta_tilt
        pan_servo.angle(curr_pan, 1000)
        tilt_servo.angle(curr_tilt, 1000)
        sensor.skip_frames(time = 1000)

        del img
        if 'diff' in locals():
            del diff
        if 'blobs' in locals():
            del blobs
        gc.collect()

        final_img = sensor.snapshot()
        final_img.draw_cross(img_cx, img_cy, color=(255, 255, 255))
        send_img(final_img)
        print(final_img.compressed_for_ide(), end='')

        target_locked = True
