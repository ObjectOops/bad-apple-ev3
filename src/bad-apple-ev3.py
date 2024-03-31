#!/usr/bin/env pybricks-micropython

import time

from pybricks.media.ev3dev import Image
from pybricks.hubs import EV3Brick
from pybricks.tools import wait

ev3 = EV3Brick()
ev3.screen.clear()

frame_count = 6572
directory = '/home/robot/bad-apple-ev3/assets/frames/'
video_length = 3 * 60 + 39 + 0.08
dt_offset = 0.413

if __name__ == '__main__':
    # We can't load a significant number of images into memory, so we'll try to do it one-by-one.
    dt = video_length / frame_count
    for i in range(1, frame_count + 1):
        t1 = time.ticks_ms() # Slightly faster than the `StopWatch` API.
        ev3.screen.load_image(directory + 'frame%04d.png' % i)
        t2 = time.ticks_ms()
        wait(dt - (t2 - t1) - dt_offset) # Higher precision (maybe) and less latency than `time.sleep_ms` due to not needing to cast.
