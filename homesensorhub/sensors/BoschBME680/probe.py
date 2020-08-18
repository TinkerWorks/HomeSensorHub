"""Module which implements the probing for the BoschBME680 sensor."""
from sensors.BoschBME680.type import TemperatureBoschBME680
from sensors.BoschBME680.type import AltitudeBoschBME680
from sensors.BoschBME680.type import HumidityBoschBME680
from sensors.BoschBME680.type import PressureBoschBME680
from sensors.BoschBME680.type import GasBoschBME680

import adafruit_bme680
import busio
import board
import logging


logging.basicConfig(level=logging.INFO)


class ProbeBoschBME680():
    """Class which implements probing for BME680 sensor."""

    ADDRESSES = [0x77, 0x76]
    I2C = busio.I2C(board.SCL, board.SDA)

    @classmethod
    def probe(cls) -> list:
        """
        Probe for Bosch BME type sensors to the possible I2C addresses.

        Function which iterates over multiple I2C addresses and look for
        sensors of the type BoschBME. In case the sensor is not found at any
        of the specified I2C address, None is returned.
        """
        for address in ProbeBoschBME680.ADDRESSES:
            try:
                sensor = cls.get_sensor_probe_function()(ProbeBoschBME680.I2C,
                                                         address)
                logging.info("{} found at {}".format(cls.get_sensor_name(),
                                                     hex(address)))
                return cls.generate_sensor_types(sensor)
            except ValueError as ve:
                logging.info("Found no {} sensor at address {}.".format(cls.get_sensor_name(),
                                                                        hex(address)))
            except RuntimeError as re:
                logging.info("The chip found at {} address has a different ID than {}." \
                             "These are not the sensors you're looking for."
                             .format(address, cls.get_sensor_name()))

    @staticmethod
    def get_sensor_probe_function():
        """Return the function used for probing the sensor."""
        return adafruit_bme680.Adafruit_BME680_I2C

    @staticmethod
    def get_sensor_name():
        """Return the name of the sensor."""
        return "BoschBME680"

    @staticmethod
    def generate_sensor_types(sensor):
        return [TemperatureBoschBME680(sensor),
                AltitudeBoschBME680(sensor),
                HumidityBoschBME680(sensor),
                PressureBoschBME680(sensor),
                GasBoschBME680(sensor)]
