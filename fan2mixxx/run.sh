#!/bin/sh

sudo xinput set-int-prop "USB Optical Mouse" "Device Enabled" 8 0

THISDIR=$(dirname $(readlink -f "$0"))
sudo schedtool -R -p 95 -n -15 -e "$THISDIR/fan2midi.py"

