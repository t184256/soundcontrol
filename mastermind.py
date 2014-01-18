#!/usr/bin/python
# written by Alexander Sosedkin, distributed under GNU GPLv3, please see LICENSE
import liblo

MIXER_ADDRESS = ('localhost', 9001)
TAB_ADDRESS = ('10.199.1.193', 9000)
AREP, ACTL = '/alsamixer_reporter/', '/alsamixer_controller/'
PORT = 8000

class LibLoTest(object):
    def __init__(self, port = None):
        self.server = liblo.Server(port)
        print "mastermind listening on URL: " + self.server.get_url()
        self.register_volume_control('Master',
                                     '/2/fader_master', '/2/toggle_master')
        self.register_volume_control('Beep', '/2/fader_beep', '/2/toggle_beep')
        self.register_volume_control('Capture', '/2/fader_mic', '/2/toggle_mic')

    def run(self):
        while True: self.server.recv(10)

    def register_volume_control(self, name, tab_path, tab_path_mute=None):
        def cb_alsa2tab_vol(path, args, types, src):
            liblo.send(TAB_ADDRESS, tab_path, *args)
        self.server.add_method(AREP + name, 'f', cb_alsa2tab_vol)
        def cb_tab2alsa_vol(path, args, types, src):
            liblo.send(MIXER_ADDRESS, ACTL + name, *args)
        self.server.add_method(tab_path, 'f', cb_tab2alsa_vol)
        if not tab_path_mute: return
        def cb_tab2alsa_mute(path, args, types, src):
            liblo.send(MIXER_ADDRESS, ACTL + name + '/mute', not bool(args[0]))
        self.server.add_method(tab_path_mute, None, cb_tab2alsa_mute)
        def cb_alsa2tab_mute(path, args, types, src):
            liblo.send(TAB_ADDRESS, tab_path_mute, float(not args[0]))
        self.server.add_method(AREP + name + '/mute', None, cb_alsa2tab_mute)

if __name__ == '__main__': LibLoTest(PORT).run()

