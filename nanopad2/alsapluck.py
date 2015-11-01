#!/usr/bin/python

import pypm, sys, time, math

DEV_NAME = 'nanoPAD2 MIDI 1'
OUT_NAME = 'fs'

def find_device(name_):
    for i in range(pypm.CountDevices()):
        interf,name,inp,outp,opened = pypm.GetDeviceInfo(i)
        if name_ == name: return i + 1

def noteon(chan, note, vel):
    midi_out.Write([[[0x90 + chan, note, vel], pypm.Time()]])

def noteoff(chan, note):
    midi_out.Write([[[0x80 + chan, note, 0], pypm.Time()]])

FIRST_NOTE = 24+12 + 4 # E, not C

out_num = find_device(OUT_NAME) - 1
if out_num == None:
    print OUT_NUM, 'not found, aborting!'
    sys.exit(1)
print OUT_NAME, 'found at number', out_num
midi_out = pypm.Output(out_num, 0)

import alsaaudio, numpy
inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, 'hw:CARD=Set')
inp.setchannels(1)
inp.setrate(48000)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
inp.setperiodsize(64)

HIGH = 500
LOW = 10
TOLERATELOW = 5
TOLERATEREONTEON = 3
ACCEPTHIGHAFTER = 2

prev = 0
on = False
tolerate = 0
accepthigh = 0
while True:
    l, d = inp.read()
    d = numpy.fromstring(d, dtype='int16')
    m = max(d, key=lambda e: abs(e))

    if m > HIGH:
        accepthigh += 1
    else:
        accepthigh = 0

    if (not on or tolerate <= TOLERATEREONTEON) and HIGH < m < prev and accepthigh > ACCEPTHIGHAFTER:
        on = True
        nv = float(m - LOW * 0.75) / 2048
        if nv > 1: nv = 1.
        nv = nv ** 2
        nv = int(nv * 127)
        print 'noteon', m, nv
        noteon(0, FIRST_NOTE, nv)
        tolerate = TOLERATELOW

    if on and m < LOW and prev < LOW and tolerate:
        tolerate -= 1
        #print 'tlow', tolerate
        if not tolerate:
            on = False
            print 'noteoff'
            noteoff(0, FIRST_NOTE)

    if m > LOW:
        tolerate = TOLERATELOW

    prev = m

inp.close()

