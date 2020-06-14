#!/usr/bin/env bash
echo "Installing Plex Wake-On-Lan"

pip3 install getmac
pip3 install wakeonlan
cp plex_wol.service /lib/systemd/system/
mkdir /usr/bin/plex_wol
cp plex_wol.py /usr/bin/plex_wol