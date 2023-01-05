"""Module which implements the probing for the BoschBME680 sensor."""
from homesensorhub.sensors.BoschBME.BoschBME680.type import TemperatureBoschBME680
from homesensorhub.sensors.BoschBME.BoschBME680.type import AltitudeBoschBME680
from homesensorhub.sensors.BoschBME.BoschBME680.type import HumidityBoschBME680
from homesensorhub.sensors.BoschBME.BoschBME680.type import PressureBoschBME680
from homesensorhub.sensors.BoschBME.BoschBME680.type import GasBoschBME680
from homesensorhub.sensors.BoschBME.probe import ProbeBoschBME

import adafruit_bme680

from homesensorhub.utils import logging
logger = logging.getLogger(__name__)


class ProbeBoschBME680(ProbeBoschBME):
    """Class which implements probing for BME680 sensor."""

    @staticmethod
    def get_sensor_probe_function():
        """Return the function used for probing the sensor."""
        return adafruit_bme680.Adafruit_BME680_I2C

    @staticmethod
    def get_sensor_name():
        """Return the name of the sensor."""
        return "BoschBME680"

    @staticmethod
    def generate_sensor_types(sensor, send_payload_callback, lock):
        return [TemperatureBoschBME680(sensor, send_payload_callback, lock),
                AltitudeBoschBME680(sensor, send_payload_callback, lock),
                HumidityBoschBME680(sensor, send_payload_callback, lock),
                PressureBoschBME680(sensor, send_payload_callback, lock),
                GasBoschBME680(sensor, send_payload_callback, lock)]
