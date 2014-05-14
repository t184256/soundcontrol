#!/usr/bin/python -B
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

# TODO: backup, cleanup, deck change (left/right clicks)

from math import sqrt, atan2, pi
from evdev import InputDevice, ecodes

import rtmidi
MidiOut = rtmidi.MidiOut(name='X220-Touchpad')
MidiOut.open_virtual_port(name='X220-Touchpad')
def pitch_bend(val, chan=0):
    val = min(max(val, -0x40), 0x40)
    return MidiOut.send_message([0xE0 + chan, 0, val+0x40])

#X_CENTER = (5559 - 1320)
#Y_CENTER = (4820 - 1361)
X_CENTER = 3500
Y_CENTER = 2750

def main():
    PATH = '/dev/input/by-path/platform-i8042-serio-1-event-mouse'
    dev = InputDevice(PATH)
    x, y = None, None
    pressure = 0
    #angle = 0
    prev_a = None
    difference = 0 # interstep difference
    for event in dev.read_loop():
        if event.type == ecodes.EV_ABS:
            if event.code in (ecodes.ABS_X, ecodes.ABS_Y, ecodes.ABS_PRESSURE):
                if event.code == ecodes.ABS_PRESSURE:
                    pressure = event.value
                    if not pressure:
                        prev_a = x = y = None
                    pitch_bend(int(max(0, pressure - 32)), 1)
                    continue
                if event.code == ecodes.ABS_X: x = event.value - X_CENTER
                if event.code == ecodes.ABS_Y: y = event.value - Y_CENTER
                if (x is None or y is None): continue
                #r = sqrt(x*x + y*y)
                #print r
                a = atan2(x, y)
                if not prev_a is None:
                    da = a - prev_a
                    if da > pi: da -= pi * 2
                    if da < -pi: da += pi * 2
                    #angle -= da / (pi * 2)
                    #print -da / (pi * 2)
                    z = -da * 45 * 10 + difference
                    w = int(z)
                    w = min(max(w, -0x40), 0x40)
                    difference = z - w
                    if abs(difference) < 0.25: difference = 0
                    #print w, difference
                    pitch_bend(w, 0)
                #print "%f\t%f\t%f" % (r, a, angle)
                prev_a = a if pressure else None

if __name__ == '__main__': main()
