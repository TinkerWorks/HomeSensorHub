from sensors.drivers.TSL258x import TSL258x as sensor_driver
from sensors.types.TSL258x.TSL258x_type import LightTSL258x
from sensors.probes.probe import Probe

import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')


class ProbeTSL258x(Probe):

    SENSOR_NAME = 'TSL258x'

    @classmethod
    def probe(cls) -> list:
        """
        Probe and configure light sensors.

        For now there is only one option, using TSL258x.
        """
        sensor = sensor_driver.probe()
        sensor.config()

        logging.debug("Found {} sensor.".format(cls.SENSOR_NAME))

        return cls.generate_sensor_types(sensor)

    def generate_sensor_types(sensor):
        return [LightTSL258x(sensor)]
