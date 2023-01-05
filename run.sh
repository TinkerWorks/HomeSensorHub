#!/bin/bash

HOST=$1

rsync -rPv --delete "$(pwd)/" $HOST:~/HomeSensorHub/

case "$2" in
    "main")
        ssh -t "${HOST}" "cd HomeSensorHub ; python3 -m homesensorhub"
        ;;
    "test")
        ssh -t "${HOST}" "cd HomeSensorHub ; nose2-3 "
        ;;
    "req")
        ssh -t "${HOST}" pip3 install -r /home/$USER/HomeSensorHub/tests/requirements.txt
        ssh -t "${HOST}" pip3 install -r /home/$USER/HomeSensorHub/requirements.txt
        ;;
    "copy")
        echo "Just copy and done"
        ;;
    *)
        exit 4
        ;;
esac
