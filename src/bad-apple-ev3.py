#!/usr/bin/env pybricks-micropython

'''
Calibrated at ~7.22 V.

Start from the EV3 brick itself to avoid audio loading discrepancies.
One may need to try multiple times before the audio is synced.
'''

from threading import Thread
from time import ticks_us, sleep_us

from pybricks.media.ev3dev import Image
from pybricks.hubs import EV3Brick

ev3 = EV3Brick()
ev3.screen.clear()
ev3.speaker.set_volume(10)
ev3.light.off()

frame_count = 6572
asset_directory = '/home/robot/bad-apple-ev3/assets/'
frame_directory = asset_directory + 'frames/'
audio_directory = asset_directory + 'audio/'
video_length = (3 * 60 + 39 + 0.08) * 1_000_000
fps_reduction = 3
dt_offset = 3_000

def play_audio():
    ev3.speaker.play_file(audio_directory + 'bad-apple-audio.wav')

def play_video():
    dt = int(video_length / frame_count)
    for i in range(1, (frame_count + 1) / fps_reduction):
        t1 = ticks_us()
        ev3.screen.load_image(frame_directory + 'frame%04d.png' % (i * fps_reduction))
        t2 = ticks_us()
        sleep_us(dt * fps_reduction - (t2 - t1) - dt_offset)

if __name__ == '__main__':
    video_thread = Thread(target=play_video)
    video_thread.start()

    play_audio()
