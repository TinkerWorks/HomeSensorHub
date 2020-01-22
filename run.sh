#!/bin/bash

rsync -aAv `pwd` pi@10.3.14.102:~/HomeSensorHub
ssh  pi@10.3.14.102 python3 /home/pi/HomeSensorHub/EnvironmentalSensor.py
