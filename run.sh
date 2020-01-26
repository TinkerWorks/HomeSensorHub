#!/bin/bash

rsync -aAv --progress --delete `pwd`/ pi@10.3.14.102:~/HomeSensorHub/
ssh -t pi@raspberry-sensor-dev python3 /home/pi/HomeSensorHub/EnvironmentalSensor.py
