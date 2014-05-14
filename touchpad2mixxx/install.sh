#!/bin/sh

THISDIR=$(dirname $(readlink -f "$0"))
echo $THISDIR

echo 'Ensure that GrabEventDevice is set to off'
echo '(for example in /usr/share/X11/xorg.conf.d/50-synaptics.conf)'

ln -sf "$THISDIR/X220-Touchpad.js" ~/.mixxx/controllers/
ln -sf "$THISDIR/X220-Touchpad.midi.xml" ~/.mixxx/controllers/

