#!/usr/bin/env pybricks-micropython

from common import *

def play_audio():
    ev3.speaker.play_file(audio_directory + "bad-apple-audio.wav")

if __name__ == "__main__":
    play(play_audio)
