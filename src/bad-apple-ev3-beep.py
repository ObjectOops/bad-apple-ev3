#!/usr/bin/env pybricks-micropython

from time import ticks_us

from common import *

mil = 1_000_000
instrument_count = 13
instrument_priorities = [
    (180.86931200000004, [5, 0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12]) # Placeholder. Instrument 5 is the melody.
]

def play_audio():
    instruments = []
    for i in range(instrument_count):
        with open("instrument_%d" % i, 'r') as fin:
            notes = []
            for line in fin.readlines():
                notes.append([float(j) for j in lines.split(' ')])
            instruments.append([i, 0, notes])
    start = total = ticks_us()
    freq = 0
    dur = 0
    while True:
        t = total - start
        if t >= video_length:
            break
        t /= mil
        priority_idx = 0
        priority = instrument_priorities[priority_idx]
        while priority[0] < t:
            priority_idx += 1
            priority = instrument_priorities[priority_idx]
        for instrument_idx in priority[1]:
            instrument = instruments[instrument_idx]
            notes = instrument[2]
            note_idx = instrument[1]
            while notes[note_idx][4] < t:
                note_idx += 1
            instrument[1] = note_idx
            note = notes[note_idx]
            if note[3] <= t:
                freq = note[0]
                dur = note[4] - t
                break
        ev3.speaker.beep(freq, dur / 1000)
        total = ticks_us()

if __name__ == "__main__":
    play(play_audio)
