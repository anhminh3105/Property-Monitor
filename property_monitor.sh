#!/bin/bash

# this simple bash application is used to set the GUI application to autorun as RASPBERRY PI logs in.
# to do this, follow these steps:
# 1. issue the command sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
# 2. put this line @/home/pi/GUI/property_monitor.sh at the end of the file
# 3. save and exit
# 4. reboot

cd GUI
trap 'kill %1; kill %2' SIGINT # this line is currently not working since alt-f4 from the GUI application does not trigger the termination of other 2 background processes.
python3 sub.py & python3 data_manage.py & python3 main.py
trap - SIGINT
