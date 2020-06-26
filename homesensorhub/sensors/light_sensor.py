#!/usr/bin/env python3
from drivers.TSL258x import *
import logging
import time


logging.basicConfig(level=logging.DEBUG)


class LightSensor:
    def __init__(self, name="undefined"):
        self.name = name
        self.data = {}

        self.probe_sensor()

    def probe_sensor(self):
        self.sensor = TSL258x.probe()
        self.sensor.config()

        # logging.debug("(light) PART NO: {}".format(self.sensor.part_no))
        # logging.debug("(light) REV NO: {}".format(self.sensor.rev_no))
        # logging.debug("(ligt) sensor: {}, self: {}".format(self.sensor, self))

    def collect_data(self, interval=10):
        # logging.debug("(ligt) collect data sensor: {}; self: {}".format(self.sensor, self))

        self.data = {
            'lux': self.sensor.read()
        }

    def get_data(self, interval=10) -> dict:
        self.collect_data(interval)
        return self.data

if __name__=="__main__":
    time.sleep(1)

    while True:
        light_sensor = LightSensor(name="light")
        data = light_sensor.get_data()

        print("Light value: {}".format(data['lux']))
        time.sleep(2)
