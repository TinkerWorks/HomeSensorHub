"""Module which implements the probing for the BoschBME680 sensor."""
from sensors.probes.probe_BoschBME280 import ProbeAdafruitBME


import adafruit_bme680
import logging


logging.basicConfig(level=logging.INFO)


class ProbeAdafruitBME680(ProbeAdafruitBME):
    """Class which implements probing for BME680 sensor."""

    def get_sensor_probe_function():
        """Return the function used for probing the sensor."""
        return adafruit_bme680.Adafruit_BME680_I2C

    def get_sensor_name():
        """Return the name of the sensor."""
        return "BoschBME680"
