#!/usr/bin/python
# written by Alexander Sosedkin, distributed under GNU GPLv3, please see LICENSE
import liblo, pyalsa.alsamixer, select

PATH = '/alsamixer_reporter/'
ADDRESS = ('localhost', 8000)
NAMES = ('Master', 'PCM', 'Capture')
CAPTURE = ('Capture',)
TIMEOUT=2

def main():
    m = pyalsa.alsamixer.Mixer(); m.attach(); m.load()
    elements = {name: pyalsa.alsamixer.Element(m, name) for name in NAMES}
    for element in elements.values(): element.set_callback(callback)
    ep = select.epoll(); ep.register(*m.poll_fds[0])
    while True:
        m.handle_events()
        if not ep.poll(timeout=TIMEOUT): # if nothing happened in TIMEOUT secs
            for element in elements.values(): callback(element)

def callback(element, index_unused=None):
    cap = element.name in CAPTURE
    mn, mx = element.get_volume_range(cap)
    vol = float(element.get_volume(0, cap) - mn) / (mx - mn)
    mute = not element.get_switch(0, cap) if element.has_switch(cap) else False
    liblo.send(ADDRESS, PATH + element.name, vol)
    liblo.send(ADDRESS, PATH + element.name + '/mute', mute)

if __name__ == "__main__": main()

