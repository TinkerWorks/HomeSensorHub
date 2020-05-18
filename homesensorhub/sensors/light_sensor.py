#!/usr/bin/env python3
from sensors.drivers.TSL258x import *
import time


class LightSensor:
    def __init__(self, name):
        self.name = name

if __name__=="__main__":

    logging.basicConfig(level=logging.DEBUG)

    tsl = TSL258x.probe()

    print ("Part Number     :", tsl.part_no)
    print ("Revision NUmber :", tsl.rev_no)

    tsl.config()
    time.sleep(1)

    while True:
        print ("Light value: %d Lux" % tsl.read())
        time.sleep(2)
