"""Module which implements the probing for the BoschBME280 sensor."""
from homesensorhub.sensors.BoschBME.BoschBME280.type import TemperatureBoschBME280
from homesensorhub.sensors.BoschBME.BoschBME280.type import AltitudeBoschBME280
from homesensorhub.sensors.BoschBME.BoschBME280.type import HumidityBoschBME280
from homesensorhub.sensors.BoschBME.BoschBME280.type import PressureBoschBME280
from homesensorhub.sensors.BoschBME.probe import ProbeBoschBME

from adafruit_bme280 import basic as adafruit_bme280

from homesensorhub.utils import logging
logger = logging.getLogger(__name__)


class ProbeBoschBME280(ProbeBoschBME):
    """Class which implements probing for BME280 sensor."""

    @staticmethod
    def get_sensor_probe_function():
        """Return the function used for probing the sensor."""
        return adafruit_bme280.Adafruit_BME280_I2C

    @staticmethod
    def get_sensor_name():
        return "BoschBME280"

    @staticmethod
    def generate_sensor_types(sensor, send_payload_callback, lock):
        return [TemperatureBoschBME280(sensor, send_payload_callback, lock),
                AltitudeBoschBME280(sensor, send_payload_callback, lock),
                HumidityBoschBME280(sensor, send_payload_callback, lock),
                PressureBoschBME280(sensor, send_payload_callback, lock)]
