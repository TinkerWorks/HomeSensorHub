"""Module which implements the light sensor functionality."""
# !/usr/bin/env python3
from sensors.drivers.TSL258x import TSL258x
from sensors.sensor import Sensor
import logging


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')


class LightSensor(Sensor):
    """Class which implements the light sensor functionality."""

    def __init__(self, sensor="undefined", name="undefined"):
        """
        Initialise the light sensor class.

        By setting up the sensor, its name and the data gathered from it.
        """
        super().__init__(sensor, name)

    def collect_data(self) -> bool:
        """
        Collect data from light sensor.

        The data from the sensor hub is measured in lux.
        """
        try:
            sensor_lux = self.sensor.read()
            self.data = {
                'lux': sensor_lux
            }

            return True
        except AttributeError as ae:
            print("The sensor was not set up: {}".format(ae))
            return False


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
        return sensors

    def get_sensors(self):
        """Return the list of found sensors."""
        return self.__sensors
