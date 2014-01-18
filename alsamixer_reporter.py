#!/usr/bin/python
# written by Alexander Sosedkin, distributed under GNU GPLv3, please see LICENSE
import liblo, pyalsa.alsamixer, select

PATH = '/alsamixer_reporter/'
ADDRESS = ('localhost', 8000)
NAMES = ('Master', 'PCM')
TIMEOUT=2

def main():
    m = pyalsa.alsamixer.Mixer(); m.attach(); m.load()
    elements = {name: pyalsa.alsamixer.Element(m, name) for name in NAMES}
    for element in elements.values(): element.set_callback(callback)
    ep = select.epoll(); ep.register(*m.poll_fds[0])
    while True:
        m.handle_events(); ep.poll(timeout=TIMEOUT)
        for element in elements.values(): callback(element)

def callback(element, index_unused=None):
    mn, mx = element.get_volume_range()
    vol = float(element.get_volume() - mn) / (mx - mn)
    liblo.send(ADDRESS, PATH + element.name, vol)

if __name__ == "__main__": main()

