#!/usr/bin/python -B
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import sys
import numpy
from time import sleep, time
from evdev import InputDevice, ecodes

import rtmidi
MidiOut = rtmidi.MidiOut(name='Fan')
MidiOut.open_virtual_port(name='Fan')
def cc_send(val, chan=0):
    return MidiOut.send_message([0xE0 + chan, 0, val])

#SCALE = 1.
#SCALE = 0.28
SCALE = 0.080
GAP = 0.15
X_TO_Y = 1.05
TRANSMISSION_SCALE = 128
CHANS = 8
#EACH = 50
EACH = 1
RUNNING_AVERAGE = 256
WEIGHT = 0.005

WEIGHTS_ = tuple(
    float( ((RUNNING_AVERAGE - i)**2) * ((i - 0)**6)) / ((RUNNING_AVERAGE/2)**8)
    for i in range(RUNNING_AVERAGE)
)
WEIGHTS = tuple(
    numpy.array(WEIGHTS_[i:] + WEIGHTS_[:i], dtype=float)
    for i in range(RUNNING_AVERAGE)
)

sys.stderr.write('start\n'); sys.stderr.flush()

#weighted_sum = lambda l: sum(l[i] * WEIGHTS[i] for i in range(RUNNING_AVERAGE))
weighted_sum = lambda a, i: numpy.inner(a, WEIGHTS[i])
#weighted_sum = lambda a, i: numpy.sum(a) / RUNNING_AVERAGE * 4
et = lambda event: event.sec + event.usec * 1.e-6

def main():
    PATH = '/dev/input/by-id/usb-192f_USB_Optical_Mouse-event-mouse'
    dev = InputDevice(PATH)
    dev.grab()

    x, y = 0, 0
    tm = ts = time()
    skippy = 0
    running_average_x = numpy.array([0] * RUNNING_AVERAGE, dtype=float)
    running_average_y = numpy.array([0] * RUNNING_AVERAGE, dtype=float)
    difference = 0. # interstep difference to be compensated later
    #avg_x, avg_y = 0., 0.
    ra = 0.

    i = 0
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
        #avg_x = avg_x * (1 - WEIGHT) + x * WEIGHT
        #avg_y = avg_y * (1 - WEIGHT) + y * WEIGHT
        running_average_x[i] = x
        running_average_y[i] = y
        ra_ = weighted_sum(running_average_x + running_average_y, i)
        ra_ /= (2 * RUNNING_AVERAGE)
        ra = ra * (1 - WEIGHT) + ra_ * WEIGHT
        s = ra
        if (s > 1) and (s < 1 + GAP): s = 1
        if (s > 1 + GAP): s = s - GAP
        if (divmod(skippy, EACH)[1] == 0):
            z = s * TRANSMISSION_SCALE + difference
            #w = int(z); w = min(max(w, -0x40), 0x40)
            w = int(z); w = min(max(w, -0x100 * CHANS), 0x100 * CHANS)
            difference = z - w;
            t = w + 0x100 * CHANS;
            cc, d = divmod(t, 0x100)
            #if abs(difference) < 0.25: difference = 0
            #print , cc * 0x100 + t - CHANS * 0x100
            cc_send(d, cc)
            #print ra
            #print ra#, ra_, 0, 1, 2
            #sys.stdout.flush()
        tm += 0.0003
        skippy += 1
        while time() - tm < 0:
            sleep(0.0001)
        i += 1
        if i == RUNNING_AVERAGE: i = 0
        #if time() - ts > 5: sys.exit(1)


if __name__ == '__main__': main()
