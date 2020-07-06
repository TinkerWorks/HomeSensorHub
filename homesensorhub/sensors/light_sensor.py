"""Module which implements the light sensor functionality."""
# !/usr/bin/env python3
from drivers.TSL258x import TSL258x
import logging
import time


logging.basicConfig(level=logging.DEBUG)


class LightSensor:
    """Class which implements the light sensor functionality."""

    def __init__(self, sensor="undefined", name="undefined"):
        self.name = name
        self.data = {}
        self.sensor = sensor

    def collect_data(self) -> bool:
        # logging.debug("(ligt) collect data sensor: {}; self: {}" \
        #   .format(self.sensor, self))
        try:
            sensor_lux = self.sensor.read()
            self.data = {
                'lux': sensor_lux
            }

            return True
        except AttributeError:
            print("The sensor was not set up.")
            return False

    def get_data(self) -> dict:
        self.collect_data()
        return self.data


class LightSensorProbe:
    """Class which probes for light sensors for data gathering."""

    def __init__(self):
        """
        Initialise the sensors list.

        In case there will be more than one light sensor, each will be found
        here.
        """
        self.__sensors = self.probe_sensors()

    def probe_sensors(self) -> list:
        """
        Probe and configure light sensors.

        For now there is only one option, using TSL258x.
        """
        sensor = TSL258x.probe()
        sensor.config()
        sensors = []

        light_sensor = LightSensor(sensor=sensor,
                                   name="light")

        sensors.append(light_sensor)

        # logging.debug("(light) PART NO: {}".format(self.sensor.part_no))
        # logging.debug("(light) REV NO: {}".format(self.sensor.rev_no))
        # logging.debug("(ligt) sensor: {},self: {}".format(self.sensor, self))

        return sensors

    def get_sensors(self):
        return self.__sensors


if __name__ == "__main__":
    ls_probe = LightSensorProbe()
    ls_probe.probe_sensors()

    while True:
        for sensor in ls_probe.get_sensors():
            data = sensor.get_data()
            logging.info(data)
            time.sleep(2)
