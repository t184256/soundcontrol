#!/bin/sh

THISDIR=$(dirname $(readlink -f "$0"))
echo $THISDIR

#ln -sf "$THISDIR/Thinklight.js" ~/.mixxx/controllers/
ln -sf "$THISDIR/Thinklight.midi.xml" ~/.mixxx/controllers/

