#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
sudo pip install websockets
export PATH="/usr/bin/python:$PATH"
cd home/spacis/shared/spacis-mbe/mbe-rpi
pip show websockets
python mbe-computer.py
cd /
