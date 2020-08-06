#!/bin/bash

HOST=$1

rsync -aAv --progress --delete "$(pwd)/" pi@$HOST:~/HomeSensorHub_$USER/

# ssh -t pi@$HOST pip3 install -r /home/pi/HomeSensorHub_$USER/requirements.txt

case "$2" in
    "main")
        ssh -t pi@$HOST PYTHONPATH=/home/pi/HomeSensorHub_$USER python3 /home/pi/HomeSensorHub_$USER/homesensorhub/__main__.py
        ;;
    *)
        exit 4
        ;;
esac
