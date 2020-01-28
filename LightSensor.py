#!/usr/bin/env python3
from TSL258x import *
import time


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
