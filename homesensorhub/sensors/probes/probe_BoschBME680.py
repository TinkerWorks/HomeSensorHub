"""Module which implements the probing for the BoschBME680 sensor."""
from sensors.probes.probe_BoschBME import ProbeAdafruitBME
from sensors.types.BoschBME.BoschBME680.temperature_BoschBME680 import TemperatureBoschBME680
from sensors.types.BoschBME.BoschBME680.altitude_BoschBME680 import AltitudeBoschBME680
from sensors.types.BoschBME.BoschBME680.humidity_BoschBME680 import HumidityBoschBME680
from sensors.types.BoschBME.BoschBME680.pressure_BoschBME680 import PressureBoschBME680
from sensors.types.BoschBME.BoschBME680.gas_BoschBME680 import GasBoschBME680

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

    def generate_sensor_types(sensor, sensor_name):
        return [TemperatureBoschBME680(sensor, sensor_name),
                AltitudeBoschBME680(sensor, sensor_name),
                HumidityBoschBME680(sensor, sensor_name),
                PressureBoschBME680(sensor, sensor_name),
                GasBoschBME680(sensor, sensor_name)]
