#!/usr/bin/python
# written by Alexander Sosedkin, distributed under GNU GPLv3, please see LICENSE
import liblo

MIXER_ADDRESS = ('localhost', 9001)
TAB_ADDRESS = ('10.199.1.193', 9000)
PORT = 8000

class LibLoTest(object):
    def __init__(self, port = None):
        self.server = liblo.Server(port)
        print "mastermind listening on URL: " + self.server.get_url()
        self.server.add_method('/2/fader_master', 'f', self.cb_fader_master)
        self.server.add_method('/alsamixer_reporter/Master', 'f', self.cb_master)

    def run(self):
        while True: self.server.recv(10)

    def cb_master(self, path, args, types, src):
        liblo.send(TAB_ADDRESS, '/2/fader_master', args[0])

    def cb_fader_master(self, path, args, types, src):
        liblo.send(MIXER_ADDRESS, '/alsamixer_controller/' + 'Master', args[0])

if __name__ == '__main__': LibLoTest(PORT).run()

