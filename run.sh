#!/bin/bash

HOST=$1

rsync -aAv --progress --delete "$(pwd)/" $HOST:~/HomeSensorHub/

LOG_FORMAT="COLOREDLOGS_LOG_FORMAT=\"%(asctime)s %(name)s - %(levelname)s -> %(message)s\""

case "$2" in
    "main")
        ssh -t "${HOST}" "cd HomeSensorHub ; ${LOG_FORMAT} python3 -m homesensorhub"
        ;;
    "test")
        ssh -t "${HOST}" "source ~/.profile ; make real-nosetest -C /home/$USER/HomeSensorHub"
        ;;
    "req")
        ssh -t "${HOST}" pip3 install -r /home/$USER/HomeSensorHub/requirements.txt
        ;;
    *)
        exit 4
        ;;
esac
