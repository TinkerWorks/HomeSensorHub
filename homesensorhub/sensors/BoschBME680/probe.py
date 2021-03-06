"""Module which implements the probing for the BoschBME680 sensor."""
from sensors.BoschBME680.type import TemperatureBoschBME680
from sensors.BoschBME680.type import AltitudeBoschBME680
from sensors.BoschBME680.type import HumidityBoschBME680
from sensors.BoschBME680.type import PressureBoschBME680
from sensors.BoschBME680.type import GasBoschBME680

from filelock import FileLock
import adafruit_bme680
import busio
import board
import os

from utils import logging
logger = logging.getLogger(__name__)


class ProbeBoschBME680():
    """Class which implements probing for BME680 sensor."""

    ADDRESSES = [0x77, 0x76]
    I2C = busio.I2C(board.SCL, board.SDA)

    @classmethod
    def probe(cls, send_payload_callback=None) -> list:
        """
        Probe for Bosch BME type sensors to the possible I2C addresses.

        Function which iterates over multiple I2C addresses and look for
        sensors of the type BoschBME. In case the sensor is not found at any
        of the specified I2C address, None is returned.
        """

        lock_file = "/var/tmp/hsh_" + cls.get_sensor_name() + ".lock"
        lock = FileLock(lock_file)

        with lock:
            try:
                os.chmod(lock_file, 0o777)
            except PermissionError:
                pass

            for address in ProbeBoschBME680.ADDRESSES:
                try:
                    sensor = cls.get_sensor_probe_function()(ProbeBoschBME680.I2C, address)
                    logger.success("{} found at {}".format(cls.get_sensor_name(), hex(address)))
                    # Initial read to re-initialize sensor.
                    # Fixes bad state when it is run in multiple instances
                    # ... sometimes ...
                    sensor.gas
                    sensor.temperature
                    sensor.humidity
                    sensor.pressure
                    return cls.generate_sensor_types(sensor, send_payload_callback, lock)
                except ValueError:
                    logger.verbose("Found no {} sensor at address {}."
                                   .format(cls.get_sensor_name(), hex(address)))
                except RuntimeError:
                    logger.verbose("The chip found at {} address has a different ID than {}."
                                   .format(hex(address), cls.get_sensor_name()))
                    logger.verbose("These are not the sensors you're looking for.")

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
