#!/usr/bin/python -B
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

from math import sqrt, atan2, pi
from evdev import InputDevice, ecodes

import rtmidi
MidiOut = rtmidi.MidiOut(name='X220-Touchpad')
MidiOut.open_virtual_port(name='X220-Touchpad')
def pitch_bend(val, chan=0):
    val = min(max(val, -0x40), 0x40)
    return MidiOut.send_message([0xE0 + chan, 0, val+0x40])

X_CENTER = 3500
Y_CENTER = 2750
R_CORNER = 2100

def main():
    PATH = '/dev/input/by-path/platform-i8042-serio-1-event-mouse'
    dev = InputDevice(PATH)
    x, y, r, a = None, None, None, None
    pressure = 0
    prev_a = None
    difference = 0 # interstep difference to be compensated later
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            if event.code == ecodes.BTN_LEFT and event.value:
                if not r is None:
                    if r > R_CORNER:
                        if -pi   < a < -pi/2: pitch_bend(4, 2)
                        if  pi/2 < a <  pi:   pitch_bend(5, 2)
                        if -pi/2 < a <  0:    pitch_bend(6, 2)
                        if  0    < a <  pi/2: pitch_bend(7, 2)
                    else:
                        pitch_bend(8, 2)
                else:
                    pitch_bend(9, 2)
        if event.type == ecodes.EV_ABS:
            if event.code in (ecodes.ABS_X, ecodes.ABS_Y, ecodes.ABS_PRESSURE):
                if event.code == ecodes.ABS_PRESSURE:
                    if event.value > 0 and not pressure and not r is None:
                        if r > R_CORNER:
                            if -pi   < a < -pi/2: pitch_bend(0, 2)
                            if  pi/2 < a <  pi:   pitch_bend(1, 2)
                            if -pi/2 < a <  0:    pitch_bend(2, 2)
                            if  0    < a <  pi/2: pitch_bend(3, 2)
                    pressure = event.value
                    if not pressure:
                        prev_a = x = y = r = a = None
                    if r <= R_CORNER:
                        pitch_bend(int(max(0, pressure - 32)), 1)
                    continue
                if event.code == ecodes.ABS_X: x = event.value - X_CENTER
                if event.code == ecodes.ABS_Y: y = event.value - Y_CENTER
                if (x is None or y is None): continue
                r = sqrt(x*x + y*y)
                a = atan2(x, y)
                if not prev_a is None and r <= R_CORNER:
                    da = a - prev_a
                    if da > pi: da -= pi * 2
                    if da < -pi: da += pi * 2
                    z = -da * 45 * 10 + difference
                    w = int(z); w = min(max(w, -0x40), 0x40)
                    difference = z - w;
                    if abs(difference) < 0.25: difference = 0
                    pitch_bend(w, 0)
                if (r > R_CORNER): pitch_bend(0, 0)
                prev_a = a if pressure else None

if __name__ == '__main__': main()
