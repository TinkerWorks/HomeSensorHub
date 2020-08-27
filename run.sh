#!/bin/bash

HOST=$1

rsync -aAv --progress --delete "$(pwd)/" $HOST:~/HomeSensorHub/

case "$2" in
    "main")
        ssh -t $HOST PYTHONPATH=/home/$USER/HomeSensorHub python3 /home/$USER/HomeSensorHub/homesensorhub/__main__.py
        ;;
    "test")
        ssh -t $HOST "source ~/.profile ; make real-nosetest -C /home/$USER/HomeSensorHub"
        ;;
    "req")
        ssh -t $HOST pip3 install -r /home/$USER/HomeSensorHub/requirements.txt
        ;;
    *)
        exit 4
        ;;
esac
