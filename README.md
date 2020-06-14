# Plex_WakeOnLan

This script allows to wake another device whenever somone in the network lauches a Plex client.\n
This can be accomplish because Plex client sends a discovery packet on port 32412 to all devices in the network.\n
The script was designed to save power on the plex server, since the server needs to have a considerable ammount of processing power to handle transcoding, by allowing it to be constantly sleeping and waking up only when needed. In order to do so, the script needs to be running on a machine always on, in my case i use a RaspberryPi.\n

To wake the target machine, it uses a magic packet.


## Install Inscructions
Make sure to have python3 and pip3 installed on the machine.

- Download the files
- Run "sudo sh install.sh"
- Run "sudo systemctl daemon-reload"
- Run "sudo systemctl enable plex_wol.service"
- Run "sudo systemctl start plex_wol.service"
