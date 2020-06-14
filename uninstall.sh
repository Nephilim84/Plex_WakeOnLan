systemctl disable plex_wol.service
systemctl stop plex_wol.service

rm -r /usr/bin/plex_wol
rm /lib/systemd/system/plex_wol.service