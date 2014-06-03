#!/usr/bin/python
import sys
from time import time, sleep

ts = time()
for l in file(sys.argv[1]).readlines():
    s = l.split()
    t = float(s[0])
    while(time() - ts < t/5): sleep(0.001)
    sys.stdout.write(eval('s[%s]' % sys.argv[2]) + '\n'); sys.stdout.flush()

