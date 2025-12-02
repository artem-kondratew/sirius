import sensor
import time
import pyb

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time=2000)
clock = time.clock()

uart = pyb.UART(3, 115200)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

TARGET_COLOR = RED
COLOR_TOLERANCE = 100

def roi_median_rgb(img, roi):
    x, y, w, h = roi
    r_vals = []
    g_vals = []
    b_vals = []
    for i in range(x, x + w):
        for j in range(y, y + h):
            r, g, b = img.get_pixel(i, j)
            r_vals.append(r)
            g_vals.append(g)
            b_vals.append(b)
    r_vals.sort()
    g_vals.sort()
    b_vals.sort()
    mid = len(r_vals) // 2
    return (r_vals[mid], g_vals[mid], b_vals[mid])


def is_color_match(pixel, target, tol):
    r, g, b = pixel
    tr, tg, tb = target
    return abs(r - tr) <= tol and abs(g - tg) <= tol and abs(b - tb) <= tol

while True:
    clock.tick()
    img = sensor.snapshot().lens_corr(1.8)

    circles = img.find_circles(
        threshold=2700,
        x_margin=10,
        y_margin=10,
        r_margin=10,
        r_min=2,
        r_max=20,
        r_step=1,
    )

    color_circles_count = 0

    for c in circles:
        x, y, r = c.x(), c.y(), c.r()
        roi_x = max(x - r, 0)
        roi_y = max(y - r, 0)
        roi_w = min(r*2, img.width() - roi_x)
        roi_h = min(r*2, img.height() - roi_y)

        roi = (roi_x, roi_y, roi_w, roi_h)
        med = roi_median_rgb(img, roi)

        print('med', med)
        if is_color_match(med, TARGET_COLOR, COLOR_TOLERANCE):
            color_circles_count += 1
            img.draw_circle(x, y, r, color=(255, 0, 255))

    uart.write(bytes([min(color_circles_count, 255)]))
    print("FPS:", clock.fps())
    print(img.compressed_for_ide(), end='')
