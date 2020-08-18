"""Module which implements the probing for the BoschBME280 sensor."""
from sensors.probes.probe_BoschBME import ProbeBoschBME
from sensors.types.BoschBME.BoschBME280.temperature_BoschBME280 import TemperatureBoschBME280
from sensors.types.BoschBME.BoschBME280.altitude_BoschBME280 import AltitudeBoschBME280
from sensors.types.BoschBME.BoschBME280.humidity_BoschBME280 import HumidityBoschBME280
from sensors.types.BoschBME.BoschBME280.pressure_BoschBME280 import PressureBoschBME280

import adafruit_bme280
import logging


logging.basicConfig(level=logging.INFO)


class ProbeBoschBME280(ProbeBoschBME):
    """Class which implements probing for BME280 sensor."""

    def get_sensor_probe_function():
        """Return the function used for probing the sensor."""
        return adafruit_bme280.Adafruit_BME280_I2C

    def get_sensor_name():
        """Return the name of the sensor."""
        return "BoschBME280"

    def generate_sensor_types(sensor):
        return [TemperatureBoschBME280(sensor),
                AltitudeBoschBME280(sensor),
                HumidityBoschBME280(sensor),
                PressureBoschBME280(sensor)]
