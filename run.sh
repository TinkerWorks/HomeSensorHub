#!/bin/bash

rsync -aAv --progress --delete `pwd`/ pi@raspberry-sensor-dev:~/HomeSensorHub_$USER/

# ssh -t pi@raspberry-sensor-dev pip3 install -r /home/pi/HomeSensorHub_$USER/requirements.txt

case "$1" in
    "env")
        ssh -t pi@raspberry-sensor-dev python3 /home/pi/HomeSensorHub_$USER/main.py
        ;;
    "motion")
        ssh -t pi@raspberry-sensor-dev python3 /home/pi/HomeSensorHub_$USER/sensors/motion_sensor.py
        ;;
    "light")
        ssh -t pi@raspberry-sensor-dev python3 /home/pi/HomeSensorHub_$USER/sensors/light_sensor.py
        ;;
    *)
        exit 4
        ;;
esac
