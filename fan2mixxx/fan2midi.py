#!/usr/bin/python -B
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import sys
import time
from math import sqrt, pi, sin
from evdev import InputDevice, ecodes

import rtmidi
MidiOut = rtmidi.MidiOut(name='Fan')
MidiOut.open_virtual_port(name='Fan')
def cc_send(val, chan=0):
    return MidiOut.send_message([0xE0 + chan, 0, val])

SCALE = 0.57
X_TO_Y = 1.05
TRANSMISSION_SCALE = 128
CHANS = 8
INJECT_ZERO_AFTER = 0.01
#FRICTION = 0.01
#FRICTION2 = 0.05
WEIGHT = 1./ 4
SPEEDMATCH = 1./ 4
WEIGHT_NEAR_ONE = 1./ 128
SPEEDMATCH_NEAR_ONE = 1./ 8
FORGIVING_NEAR_ONE = 0.33
FORGIVING_NEAR_ONE_HIGHER_THAN = 3
FORGIVING_NEAR_ONE_LOWER_THAN = 2
FORGIVING_ADJUST_SCALE = 0.01
FORGIVING_ADJUST_SCALE_BY = 0.0025
TEND_TO_ONE = 0.03
#tend_to_one_strength = lambda d1_n: d1_n**2 * (1-d1_n)**2 / 0.0625
tend_to_one_strength = lambda d1_n: (1-d1_n)**(1./5)


et = lambda event: event.sec + event.usec * 1.e-6

def main():
    PATH = '/dev/input/by-id/usb-192f_USB_Optical_Mouse-event-mouse'
    dev = InputDevice(PATH)
    dev.grab()

    target = target_real = transmitted = 0.
    delta_prev = 0.
    x, y, t_prev = 0., 0., time.time()
    v_prev = 0.
    sys.stderr.write('start\n'); sys.stderr.flush()
    ts = t_now = time.time()
    i = 32
    scale = SCALE
    while True:
        time.sleep(0.0005)
        real_event = False
        try:
            e = dev.read_one()
            if e.type == ecodes.EV_REL:
                if e.code == ecodes.REL_X:
                    x = float(e.value) / scale
                else:
                    y = float(-e.value) / (scale * X_TO_Y)
            if e.type == ecodes.EV_SYN:
                t_now = et(e)
                real_event = True
            if not real_event: continue
        except:
            if time.time() - t_now < INJECT_ZERO_AFTER: continue
            x, y, t_now = 0., 0., time.time()
            real_event = False

        #dt = t_now - t_prev
        s = (x + y) / 2

        if i > 0:
            i -= 1
            continue

        dtt = target - transmitted
        if abs(v_prev - 1.) < TEND_TO_ONE * 0.8:
            if dtt > FORGIVING_NEAR_ONE_HIGHER_THAN:
                target -= FORGIVING_NEAR_ONE
                #sys.stderr.write('forg-\n'); sys.stderr.flush()
            if dtt < -FORGIVING_NEAR_ONE_LOWER_THAN:
                target += FORGIVING_NEAR_ONE
                #sys.stderr.write('forg+\n'); sys.stderr.flush()
        dtt = target - transmitted

        target += s
        target_real += s
        delta = target - transmitted
        if abs(v_prev - 1.) > TEND_TO_ONE * 0.9:
            v = delta * SPEEDMATCH
            v = v_prev * (1 - WEIGHT) + v * WEIGHT
        else:
            v = delta * SPEEDMATCH_NEAR_ONE
            v = v_prev * (1 - WEIGHT_NEAR_ONE) + v * WEIGHT_NEAR_ONE
        #v_delta = v - v_prev
        #v_capped = 0
        #if abs(v_delta) > FRICTION2:
        #    v_capped = v_delta / abs(v_delta) * 2
        #    v_sign = v_delta / abs(v_delta)
        #    v_delta -= FRICTION2 * v_sign
        #elif abs(v_delta) > FRICTION:
        #    v_capped = v_delta / abs(v_delta)
        #    v_sign = v_delta / abs(v_delta)
        #    v_delta -= FRICTION * v_sign
        #v = v_prev + v_delta

        d1 = v - 1.
        if abs(d1) < TEND_TO_ONE:
            # in interval (-R, R), R = TEND_TO_ONE
            # change d1 to d1 + TEND_TO_ONE_STRENGTH * sin(d1*2*pi/R)/(2*pi*R)
            K = 2. * pi / TEND_TO_ONE
            d1_norm = abs(d1) / TEND_TO_ONE
            d1 = d1 + tend_to_one_strength(d1_norm) * sin(pi + d1 * K) / K
            v = 1 + d1
            if abs(v_prev - 1.) < abs(d1):
                scale += FORGIVING_ADJUST_SCALE_BY * d1
                if d1 > +FORGIVING_ADJUST_SCALE:
                    sys.stderr.write('scale+ %s\n' % str(scale))
                    sys.stderr.flush()
                if d1 < -FORGIVING_ADJUST_SCALE:
                    sys.stderr.write('scale- %s\n' % str(scale))
                    sys.stderr.flush()

        w = round(v * TRANSMISSION_SCALE, 0)
        w = min(max(w, -0x80 * CHANS), 0x80 * CHANS)
        d_transmitted = float(w) / TRANSMISSION_SCALE
        transmitted += d_transmitted

        cc, d = divmod(w + 0x80 * CHANS, 0x80)
        cc_send(d, cc)
        print v, dtt, -1, 2; sys.stdout.flush()
        if (time.time() > ts + 8): sys.exit(1)
        x, y, t_prev = 0., 0., t_now
        delta_prev = delta
        v_prev = v


if __name__ == '__main__': main()
