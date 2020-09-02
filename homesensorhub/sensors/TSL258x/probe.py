from sensors.TSL258x.driver import TSL258x
from sensors.TSL258x.type import LightTSL258x
from sensors.probe import Probe
from filelock import FileLock
import os

from utils import logging
logger = logging.getLogger(__name__)


class ProbeTSL258x(Probe):

    SENSOR_NAME = 'TSL258x'

    @classmethod
    def probe(cls, send_payload_callback=None) -> list:
        """Probe board for TSL258x sensor."""

        lock_file = "/var/tmp/hsh_" + cls.SENSOR_NAME + ".lock"
        lock = FileLock(lock_file)

        with lock:
            try:
                os.chmod(lock_file, 0o777)
            except PermissionError:
                pass

            sensor = TSL258x.probe()
            sensor.config()

        logger.debug("Found {} sensor.".format(cls.SENSOR_NAME))

        return cls.generate_sensor_types(sensor, send_payload_callback, lock)

    def generate_sensor_types(sensor, send_payload_callback, lock):
        return [LightTSL258x(sensor, send_payload_callback, lock)]
