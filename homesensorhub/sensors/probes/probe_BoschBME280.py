"""Module which implements the probing for the BoschBME280 sensor."""
from sensors.probes.probe_BoschBME import ProbeAdafruitBME
from sensors.types.BoschBME.temperature_BoschBME280 import TemperatureBoschBME280
from sensors.types.BoschBME.altitude_BoschBME280 import AltitudeBoschBME280
from sensors.types.BoschBME.humidity_BoschBME280 import HumidityBoschBME280
from sensors.types.BoschBME.pressure_BoschBME280 import PressureBoschBME280

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
        return [TemperatureBoschBME280(sensor, sensor_name),
                AltitudeBoschBME280(sensor, sensor_name),
                HumidityBoschBME280(sensor, sensor_name),
                PressureBoschBME280(sensor, sensor_name)]
