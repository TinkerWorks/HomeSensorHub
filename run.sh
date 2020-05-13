#!/bin/bash

HOST=$1

rsync -aAv --progress --delete "$(pwd)/" pi@$HOST:~/HomeSensorHub_$USER/

# ssh -t pi@$HOST pip3 install -r /home/pi/HomeSensorHub_$USER/requirements.txt

case "$2" in
    "env")
        ssh -t pi@$HOST python3 /home/pi/HomeSensorHub_$USER//sensors/environmental_sensor.py
        ;;
    "motion")
        ssh -t pi@$HOST python3 /home/pi/HomeSensorHub_$USER/sensors/motion_sensor.py
        ;;
    "light")
        ssh -t pi@$HOST python3 /home/pi/HomeSensorHub_$USER/sensors/light_sensor.py
        ;;
    "mqtt")
        ssh -t pi@$HOST python3 /home/pi/HomeSensorHub_$USER/communication/data_sender.py
        ;;
    "hub")
        ssh -t pi@$HOST python3 /home/pi/HomeSensorHub_$USER/communication/sensor_hub.py
        ;;
    "main")
        ssh -t pi@$HOST python3 /home/pi/HomeSensorHub_$USER/__init__.py
        ;;
    *)
        exit 4
        ;;
esac
