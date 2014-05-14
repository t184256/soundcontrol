#!/usr/bin/python -B
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

def notify(text):
    import os
    os.system('notify-send -t 500 -i play "%s" "%s"' % ('MIDITrackpoint', text))

### trackpoint disabling ###

def trackpoint(enable=True):
    import os
    cmd = 'xinput set-int-prop "PS/2 Generic Mouse"  "Device Enabled" 8 '
    cmd += '1' if enable else '0'
    os.system(cmd)

### MIDI ###

import rtmidi

MidiOut = rtmidi.MidiOut(name='MidiTrackpoint')
MidiOut.open_virtual_port(name='MidiTrackpoint')
def pitch_bend(val, chan=0):
    val = min(max(val, -0x40), 0x40)
    return MidiOut.send_message([0xE0 + chan, 0, val+0x40])

### Control ###

#def smoother_generate(weight_prev, weight_curr):
#    def smooth(val_prev, val_curr):
#        return float(val_prev) * weight_prev + float(val_curr) * weight_curr
#    return smooth

class Control(object):
    def __init__(self, rel=False, value=0, mul=1,
                 clip_lo_hi=None, tend_to_zero=None,# smoothing=None,
                 callback=None):
        self.value = value
        self.callback = callback
        self.rel, self.mul = rel, mul
        self.clip_lo_hi, self.tend_to_zero = clip_lo_hi, tend_to_zero
        if clip_lo_hi: self.lo, self.hi = clip_lo_hi
        if tend_to_zero: self.factor, self.zero = tend_to_zero
#        if smoothing:
#            self.smoother = smoother_generate(*smoothing)
#        else:
#            self.smoother = lambda prev, curr: float(curr)
    def update(self, value=None):
        prev_value = self.value
        if value != None:
            if self.rel:
                #self.value += self.smoother(prev_value, value) * self.mul
                self.value += value * self.mul
            else:
                #self.value = self.smoother(prev_value, value) * self.mul
                self.value = value * self.mul
        if self.tend_to_zero:
            self.value = self.value * self.factor \
                    if abs(self.value) > self.zero else 0
        if self.clip_lo_hi: self.value = min(max(self.value, self.lo), self.hi)
        if prev_value != self.value:
            if self.callback: self.callback(self.value)

def crossfade(val): pitch_bend(val, chan=0)#; print 'xfade', val
c_crossfade = Control(True, 0, 0.5, (-64, 63), callback=crossfade)

def bend1(val): pitch_bend(val, chan=1); print 'bend1', val
c_bend1 = Control(False, 32, 1.4, (-64, 63), (0.98, 0.5), callback=bend1)

def bend2(val): pitch_bend(val, chan=2);# print 'bend2', val
c_bend2 = Control(False, 32, 1.4, (-64, 63), (0.98, 0.5),
                # smoothing=(0.99, 0.01),
                  callback=bend2)

c_none = Control()

control_sets = [
    [ c_none, c_none ],
    [ c_crossfade, c_none ],
    [ c_bend1, c_none ],
    [ c_bend2, c_none ]
]
control_set_n = 0

### evdev ###

from evdev import Device

class MIDITrackpoint(Device):
    def update(self, event):
        global control_sets, control_set_n
        control_set = control_sets[control_set_n]
        if event.type == 'EV_REL':
            if event.code == 'REL_X':
                control_set[0].update(float(event.value))
            elif event.code == 'REL_Y':
                control_set[1].update(float(event.value))

        elif event.type == 'EV_KEY':
            if event.code == 'BTN_MIDDLE':
                if event.value == 1:
                    control_set_n += 1
                    if control_set_n == len(control_sets):
                        control_set_n = 0

                    if control_set_n == 0:
                        trackpoint(True)
                    else:
                        trackpoint(False)

                    notify('mode %d' % control_set_n)
#            elif event.code == 'BTN_LEFT':
#                pitch_bend(event.value, chan=(7 + 1))
#            elif event.code == 'BTN_RIGHT':
#                pitch_bend(event.value, chan=(7 + 3))

### GO ###

import time
PATH = '/dev/input/by-path/platform-i8042-serio-1-event-mouse'
d = MIDITrackpoint(PATH)
while True:
    d.poll()
    control_set = control_sets[control_set_n]
    for c in control_set: c.update()
    time.sleep(0.005)

