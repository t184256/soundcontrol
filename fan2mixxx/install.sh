#!/bin/sh

THISDIR=$(dirname $(readlink -f "$0"))
echo $THISDIR

#echo 'Ensure that GrabEventDevice is set to off'
#echo '(for example in /usr/share/X11/xorg.conf.d/50-synaptics.conf)'

ln -sf "$THISDIR/Fan.js" ~/.mixxx/controllers/
ln -sf "$THISDIR/Fan.midi.xml" ~/.mixxx/controllers/

