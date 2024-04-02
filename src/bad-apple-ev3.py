#!/usr/bin/env pybricks-micropython

"""
Calibrated at ~7.22 V.

Start from the EV3 brick itself to avoid audio loading discrepancies.
One may need to try multiple times before the audio is synced.
"""

import os
from threading import Thread
from time import ticks_us, sleep_us

from pybricks.media.ev3dev import Image
from pybricks.hubs import EV3Brick

asset_directory = "/home/robot/bad-apple-ev3/assets/"
frame_directory = asset_directory + "frames/"
audio_directory = asset_directory + "audio/"
video_length = (3 * 60 + 39 + 0.08) * 1_000_000
frame_count = 6572 # 30 FPS max.
target_fps = 13
dt_offset = 3_000

fps_reduction = 30 / target_fps

ev3 = EV3Brick()

ev3.speaker.set_volume(10)
ev3.screen.clear()
ev3.light.off()

done = False

def play_audio():
    ev3.speaker.play_file(audio_directory + "bad-apple-audio.wav")

def play_video():
    global done
    dt = int(video_length / frame_count)
    for i in range(1, (frame_count + 1) / fps_reduction):
        t1 = ticks_us()
        ev3.screen.load_image("frame%04d.png" % int(i * fps_reduction))
        t2 = ticks_us()
        sleep_us(int(dt * fps_reduction - (t2 - t1) - dt_offset))
    done = True

if __name__ == "__main__":
    os.chdir(frame_directory)

    video_thread = Thread(target=play_video)
    video_thread.start()

    play_audio()

    while not done:
        sleep_us(10_000)
