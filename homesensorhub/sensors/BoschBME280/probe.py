"""Module which implements the probing for the BoschBME280 sensor."""
from sensors.BoschBME280.type import TemperatureBoschBME280
from sensors.BoschBME280.type import AltitudeBoschBME280
from sensors.BoschBME280.type import HumidityBoschBME280
from sensors.BoschBME280.type import PressureBoschBME280

import adafruit_bme280
import busio
import board
import logging


logging.basicConfig(level=logging.INFO)


class ProbeBoschBME280():
    """Class which implements probing for BME280 sensor."""

    ADDRESSES = [0x77, 0x76]
    I2C = busio.I2C(board.SCL, board.SDA)

    @classmethod
    def probe(cls) -> list:
        """
        Probe for Bosch BME type sensors to the possible I2C addresses.

        Function which iterates over multiple I2C addresses and looks for sensors of the type
        BoschBME. In case the sensor is not found at the specified I2C address, None is returned.
        """
        for address in ProbeBoschBME280.ADDRESSES:
            try:
                sensor = cls.get_sensor_probe_function()(ProbeBoschBME280.I2C,
                                                         address)
                logging.info("{} found at {}".format(cls.get_sensor_name(),
                                                     hex(address)))
                return cls.generate_sensor_types(sensor)
            except ValueError:
                logging.info("Found no {} sensor at address {}.".format(cls.get_sensor_name(),
                                                                        hex(address)))
            except RuntimeError:
                logging.info("The chip found at {} address has a different ID than {}."
                             "These are not the sensors you're looking for."
                             .format(address, cls.get_sensor_name()))

    @staticmethod
    def get_sensor_probe_function():
        """Return the function used for probing the sensor."""
        return adafruit_bme280.Adafruit_BME280_I2C

    @staticmethod
    def get_sensor_name():
        return "BoschBME280"

    @staticmethod
    def generate_sensor_types(sensor):
        return [TemperatureBoschBME280(sensor),
                AltitudeBoschBME280(sensor),
                HumidityBoschBME280(sensor),
                PressureBoschBME280(sensor)]
