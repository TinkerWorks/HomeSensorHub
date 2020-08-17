"""Module which implements the probing for the BoschBME280 sensor."""
from sensors.probes.probe_BoschBME import ProbeAdafruitBME
from sensors.types.temperature_BoschBME280 import TemperatureAdafruitBME280

import adafruit_bme280
import logging


logging.basicConfig(level=logging.INFO)


class ProbeAdafruitBME280(ProbeAdafruitBME):
    """Class which implements probing for BME280 sensor."""

    def get_sensor_probe_function():
        """Return the function used for probing the sensor."""
        return adafruit_bme280.Adafruit_BME280_I2C

    def get_sensor_name():
        """Return the name of the sensor."""
        return "BoschBME280"

    def generate_sensor_types(sensor, sensor_name):
        return [TemperatureAdafruitBME280(sensor, sensor_name)]
