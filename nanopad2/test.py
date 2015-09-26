#!/usr/bin/python

import pypm, sys

DEV_NAME = 'nanoPAD2 MIDI 1'
OUT_NAME = 'fs'
PADS1 = range(51, 35, -2)
PADS2 = range(50, 34, -2)

shorten_bools = lambda bool_list: ''.join(('0' if b else '.' for b in bool_list))

def find_device(name_):
    for i in range(pypm.CountDevices()):
        interf,name,inp,outp,opened = pypm.GetDeviceInfo(i)
        if name_ == name: return i + 1

dev_num = find_device(DEV_NAME)
if dev_num == None:
    print DEV_NAME, 'not found, aborting!'
    sys.exit(1)
print DEV_NAME, 'found at number', dev_num
out_num = find_device(OUT_NAME) - 1
if out_num == None:
    print OUT_NUM, 'not found, aborting!'
    sys.exit(1)
print OUT_NAME, 'found at number', out_num

midi_in = pypm.Input(dev_num)
#midi_out = pypm.Output(pypm.GetDefaultOutputDeviceID(), 0)
midi_out = pypm.Output(out_num, 0)

pressed = False
pads1_pressed = [False] * 8
pads2_pressed = [False] * 8
note = 0
while True:
    while not midi_in.Poll(): pass
    midi_data = midi_in.Read(1) # read only 1 message at a time
    t = midi_data[0][1]
    a, b, c, d = midi_data[0][0][0], midi_data[0][0][1], midi_data[0][0][2], midi_data[0][0][3]
    if a == 176:
        # touchpad
        if b == 16:
            pressed = (c == 127)
            if pressed:
                midi_out.Write([[[0x90+0, 48 + 0, c], pypm.Time()]])
                print 'on'
            else:
                midi_out.Write([[[0x80+0, 48 + 0, c], pypm.Time()]])
                print 'off'
        else:
            continue
    elif a == 144:
        # pad pressed
        if b in PADS1: pads1_pressed[PADS1.index(b)] = True
        if b in PADS2: pads2_pressed[PADS2.index(b)] = True
    elif a == 128:
        if b in PADS1: pads1_pressed[PADS1.index(b)] = False
        if b in PADS2: pads2_pressed[PADS2.index(b)] = False
    #else:
    #    continue
    note = max([i if p else 0 for i, p in zip(range(1, 8+2), pads1_pressed)])
    midi_out.Write([[[0xb0+0, 0x00, 0x10, 0], pypm.Time()]])
    midi_out.Write([[[0xe0+0, 0, 0x40 + note * 0x4, c], pypm.Time()]])
    #print [i if p else 0 for i, p in zip(range(1, 8+2), pads1_pressed)]
    print t, a, b, c, d, '\t', 'X' if pressed else '_', note
    print shorten_bools(pads1_pressed),
    print shorten_bools(pads2_pressed)
del midi_in

