#!/usr/bin/env pybricks-micropython

"""
The maximum fixed FPS is somewhere around 13 frames per second.
Using the variable framerate display function might achieve slightly higher results.
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
variable_fps = True
frame_count = 6572 # 30 FPS max.
target_fps = 12
dt_offset = 3_000

fps_reduction = 30 / target_fps

ev3 = EV3Brick()

ev3.speaker.set_volume(10)
ev3.screen.clear()
ev3.light.off()

done = False

def play_audio():
    ev3.speaker.play_file(audio_directory + "bad-apple-audio.wav")

# Frames are loaded one by one since there's a tough memory limit 
# and the TI am1808 ARM microprocessor is single core anyways.
# The C-function that the Pybricks API binds to forces one to use PNGs.
# The ev3dev Python display bindings are not compatible with MicroPython 
# and will probably be too slow.

def play_video_fixed_fps(frames):
    print("Using fixed FPS.")
    global done
    dt = int(video_length / frame_count * fps_reduction - dt_offset)
    for i in frames:
        t1 = ticks_us()
        ev3.screen.load_image(i)
        t2 = ticks_us()
        sleep_us(dt - (t2 - t1))
        # print(dt - (t2 - t1))
    done = True

def play_video_variable_fps():
    print("Using variable FPS.")
    global done
    start = ticks_us()
    while not done:
        # Sometimes, the tick function bugs out and returns a value that results in a negative integer.
        # If a runtime error occurs because the frames went slightly too far, then so be it.
        ev3.screen.load_image("frame%04d.png" % (max(0, ticks_us() - start) / video_length * frame_count + 1))

if __name__ == "__main__":
    os.chdir(frame_directory)

    frames = ["frame%04d.png" % (i * fps_reduction) for i in range(1, int((frame_count + 1) / fps_reduction))]

    if variable_fps:
        video_thread = Thread(target=play_video_variable_fps)
    else:
        video_thread = Thread(target=play_video_fixed_fps, args=[frames])
    video_thread.start()

    play_audio()

    if variable_fps:
        done = True
    else:
        while not done:
            sleep_us(10_000)
