#!/bin/sh

sudo xinput set-int-prop "USB Optical Mouse" "Device Enabled" 8 0

sudo chmod 666 /sys/class/leds/tpacpi\:\:thinklight/brightness

THISDIR=$(dirname $(readlink -f "$0"))
sudo schedtool -R -p 95 -n -15 -e "$THISDIR/motor2midi"

