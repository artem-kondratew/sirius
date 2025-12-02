import sensor, image, time, math, pyb

threshold_index = 0

thresholds = [
    (30, 100, 15, 127, 15, 127),     # 0: красный
    (30, 100, -64, -8, -32, 32),     # 1: зелёный
    (0, 30, 0, 64, -128, 0)          # 2: синий
]

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)
clock = time.clock()

uart = pyb.UART(3, 115200, timeout_char=1000)

while True:
    clock.tick()
    img = sensor.snapshot().lens_corr(1.8)

    color_th = thresholds[threshold_index]
    blobs = img.find_blobs([color_th],
                           pixels_threshold=200,
                           area_threshold=200,
                           merge=True)
    for blob in blobs:
        x, y, w, h = blob.rect()
        img.draw_rectangle(blob.rect(), color=(0, 0, 0))
        img.draw_cross(blob.cx(), blob.cy(), color=(0, 0, 0))

    uart.write(bytes([min(len(blobs), 9)]))
    print("FPS:", clock.fps())
    print(img.compressed_for_ide(), end='')
