#!/usr/bin/env pybricks-micropython

import os

from common import *

def play_audio():
    ev3.speaker.play_file(os.path.join(audio_directory, "bad-apple-audio.wav"))

if __name__ == "__main__":
    play(play_audio)
