#!/bin/sh

THISDIR=$(dirname $(readlink -f "$0"))
echo $THISDIR

ln -sf "$THISDIR/Motor.js" ~/.mixxx/controllers/
ln -sf "$THISDIR/Motor.midi.xml" ~/.mixxx/controllers/

