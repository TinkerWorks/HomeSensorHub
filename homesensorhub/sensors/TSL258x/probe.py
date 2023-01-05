from homesensorhub.sensors.TSL258x.driver import TSL258x
from homesensorhub.sensors.TSL258x.type import LightTSL258x
from homesensorhub.sensors.probe import Probe

from homesensorhub.utils import logging
logger = logging.getLogger(__name__)


class ProbeTSL258x(Probe):

    SENSOR_NAME = 'TSL258x'

    @staticmethod
    def functional_probe(cls, send_payload_callback=None, lock=None):
        sensor = TSL258x.probe()
        sensor.config()

        logger.debug("Found {} sensor.".format(cls.get_sensor_name()))

        return cls.generate_sensor_types(sensor, send_payload_callback, lock)

    @staticmethod
    def get_sensor_name():
        return 'TSL258x'

    def generate_sensor_types(sensor, send_payload_callback, lock):
        return [LightTSL258x(sensor, send_payload_callback, lock)]
