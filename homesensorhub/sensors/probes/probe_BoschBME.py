"""Module which contains sketch the probing the BoschBME sensors."""

import board
import busio
import logging


logging.basicConfig(level=logging.INFO)


class ProbeAdafruitBME():
    """Class which implements probing for BoschBME sensors."""

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

        for address in ProbeAdafruitBME.ADDRESSES:
            try:
                sensor = cls.get_sensor_probe_function()(ProbeAdafruitBME.I2C,
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
