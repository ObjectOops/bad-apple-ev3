#!/usr/bin/env pybricks-micropython

import os
from time import ticks_us, sleep_us

from common import *

from pybricks.ev3devices import Motor
from pybricks.parameters import Port

mil = 1_000_000
instrument_count = 13
instrument_priorities = [
    (180.86931200000004, [5, 0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12]) # Placeholder. Instrument 5 is the melody.
]

motor_ports = [Port.A, Port.C, Port.D] # Placeholder.
motor_count = len(motor_ports)

port_chip_mapping = {
    Port.A : "pwmchip9/pwm1", 
    Port.B : "pwmchip9/pwm0", 
    Port.C : "pwmchip5/pwm0", 
    Port.D : "pwmchip6/pwm0"
}

dc_max = 1_000_000

cycle_wait = 100_000

def set_pwm(port: Port, period: int, dc: int):
    # Main reference: https://github.com/ev3dev/ev3dev/issues/121
    pwm_driver = port_chip_mapping[port]
    with open(os.path.join("/sys/class/pwm", pwm_driver, "period")) as dout:
        dout.write(str(period))
    with open(os.path.join("/sys/class/pwm", pwm_driver, "duty_cycle")) as dout:
        dout.write(str(dc))
    # with open(os.path.join("/sys/class/pwm", pwm_driver, "enable")) as dout:
    #     dout.write("1")

def notevelocity2dc(velocity: float) -> int:
    return int(velocity / 217 * dc_max)

def play_audio():
    instruments = []
    for i in range(instrument_count):
        with open("instrument_%d" % i, 'r') as fin:
            notes = []
            for line in fin.readlines():
                notes.append([float(j) for j in lines.split(' ')])
            instruments.append([i, 0, notes])
    start = total = ticks_us()
    freq = [[0, 0] for i in range(motor_count)]
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
        for i in range(motor_count):
            playing = False
            for instrument_idx in priority[1]:
                instrument = instruments[instrument_idx]
                notes = instrument[2]
                note_idx = instrument[1]
                while notes[note_idx][4] < t:
                    note_idx += 1
                instrument[1] = note_idx
                note = notes[note_idx]
                if note[3] <= t and note[3] not in freq:
                    freq[i] = [note[0], note[1]]
                    playing = True
                    break
            if not playing:
                freq[i] = [0, 0]
        for i, (f, v) in enumerate(freq):
            set_pwm(motor_ports[i], int(1 / f), notevelocity2dc(v))
        sleep_us(cycle_wait)
        total = ticks_us()

if __name__ == "__main__":
    play(play_audio)
