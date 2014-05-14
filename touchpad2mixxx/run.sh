#!/bin/sh

THISDIR=$(dirname $(readlink -f "$0"))
sudo schedtool -R -p 95 -n -15 -e "$THISDIR/touchpad2midi.py"

