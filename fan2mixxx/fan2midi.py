#!/usr/bin/python -B
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import sys
from time import sleep, time
from evdev import InputDevice, ecodes

import rtmidi
MidiOut = rtmidi.MidiOut(name='Fan')
MidiOut.open_virtual_port(name='Fan')
def pitch_bend(val, chan=0):
    val = min(max(val, -0x40), 0x40)
    return MidiOut.send_message([0xE0 + chan, 0, val+0x40])

et = lambda event: event.sec + event.usec * 1.e-6

#SCALE = 9.
SCALE = 0.28
#SCALE = 0.35
X_TO_Y = 1.05
EACH = 1
#EACH = 10
RUNNING_AVERAGE = 77
WEIGHT = 0.01

def main():
    PATH = '/dev/input/by-id/usb-192f_USB_Optical_Mouse-event-mouse'
    dev = InputDevice(PATH)
    dev.grab()

    avg_x, avg_y = 0., 0.

    x, y = 0, 0
    tm = sm = time()
    skippy = 0
    running_average_x = [0] * RUNNING_AVERAGE
    running_average_y = [0] * RUNNING_AVERAGE
    difference = 0. # interstep difference to be compensated later

    while True:
        x, y = 0., 0.
        try:
            e = dev.read_one()
            if e.type == ecodes.EV_REL:
                if e.code == ecodes.REL_X:
                    x = float(e.value) / SCALE
                else:
                    y = float(-e.value) / (SCALE * X_TO_Y)
            if e.type == ecodes.EV_SYN: x, y = 0, 0
        except:
            e = None
            x, y = 0, 0
        running_average_x.append(avg_x)
        running_average_x = running_average_x[1:]
        running_average_y.append(avg_y)
        running_average_y = running_average_y[1:]
        avg_x = avg_x * (1 - WEIGHT) + x * WEIGHT
        avg_y = avg_y * (1 - WEIGHT) + y * WEIGHT
        ra = (sum(running_average_x) + sum(running_average_y))
        ra /= (2 * RUNNING_AVERAGE)
        s = ra
        if (s > 1) and (s < 1.15): s = 1
        if (s > 1.15): s = s - 0.15
        if (divmod(skippy, EACH)[1] == 0):
            z = s * 32 + difference
            w = int(z); w = min(max(w, -0x40), 0x40)
            difference = z - w;
            #if abs(difference) < 0.25: difference = 0
            pitch_bend(w, 0)
            #print s
            #print ra, (avg_x + avg_y) / 2, 0, 1, 2
            #sys.stdout.flush()
        tm += 0.001
        skippy += 1
        while time() - tm < 0:
            sleep(0.0001)
        #if time() - sm > 5: sleep(4)

if __name__ == '__main__': main()
