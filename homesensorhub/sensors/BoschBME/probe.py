import busio
import board

from homesensorhub.sensors.probe import Probe

from homesensorhub.utils import logging
logger = logging.getLogger(__name__)


class ProbeBoschBME(Probe):

    ADDRESSES = [0x77, 0x76]
    I2C = busio.I2C(board.SCL, board.SDA)

    @staticmethod
    def functional_probe(cls, send_payload_callback=None, lock=None):
        """
        Probe for Bosch BME type sensors to the possible I2C addresses.

        Function which iterates over multiple I2C addresses and looks for sensors of the type
        BoschBME. In case the sensor is not found at the specified I2C address, None is returned.
        """

        for address in cls.ADDRESSES:
            try:
                sensor = cls.get_sensor_probe_function()(cls.I2C, address)
                logger.success("{} found at {}".format(cls.get_sensor_name(), hex(address)))
                # Initial read to re-initialize sensor.
                # Fixes bad state when it is run in multiple instances
                # ... sometimes ...
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
