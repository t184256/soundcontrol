#!/usr/bin/python
# written by Alexander Sosedkin, distributed under GNU GPLv3, please see LICENSE
import liblo, pyalsa.alsamixer

PATH = '/alsamixer_controller/'
NAMES = ('Master', 'PCM')
PORT = 9001

def main():
    server = liblo.Server(PORT)
    print "alsamixer_controller listening on URL: " + server.get_url()
    m = pyalsa.alsamixer.Mixer(); m.attach(); m.load()
    for name in NAMES:
        element = pyalsa.alsamixer.Element(m, name)
        server.add_method(PATH + element.name, 'f', callback, element)
    while True:
        server.recv(100); m.handle_events();

def callback(path, args, types, src, element):
    mn, mx = element.get_volume_range()
    element.set_volume_all(int(args[0] * (mx - mn) + mn))

if __name__ == "__main__": main()

