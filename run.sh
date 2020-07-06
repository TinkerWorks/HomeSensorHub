#!/bin/bash

HOST=$1

rsync -aAv --progress --delete "$(pwd)/" pi@$HOST:~/HomeSensorHub_$USER/

# ssh -t pi@$HOST pip3 install -r /home/pi/HomeSensorHub_$USER/requirements.txt

case "$2" in
    "env")
        ssh -t pi@$HOST PYTHONPATH=/home/pi/HomeSensorHub_$USER python3 /home/pi/HomeSensorHub_$USER/homesensorhub/sensors/environmental_sensor.py
        ;;
    "motion")
        ssh -t pi@$HOST PYTHONPATH=/home/pi/HomeSensorHub_$USER python3 /home/pi/HomeSensorHub_$USER/homesensorhub/sensors/motion_sensor.py
        ;;
    "light")
        ssh -t pi@$HOST PYTHONPATH=/home/pi/HomeSensorHub_$USER python3 /home/pi/HomeSensorHub_$USER/homesensorhub/sensors/light_sensor.py
        ;;
    "mqtt")
        ssh -t pi@$HOST PYTHONPATH=/home/pi/HomeSensorHub_$USER python3 /home/pi/HomeSensorHub_$USER/homesensorhub/communication/data_sender.py
        ;;
    "hub")
        ssh -t pi@$HOST PYTHONPATH=/home/pi/HomeSensorHub_$USER python3 /home/pi/HomeSensorHub_$USER/homesensorhub/communication/sensor_sink.py
        ;;
    "main")
        ssh -t pi@$HOST PYTHONPATH=/home/pi/HomeSensorHub_$USER python3 /home/pi/HomeSensorHub_$USER/homesensorhub/__init__.py
        ;;
    *)
        exit 4
        ;;
esac
