"""
Module which implements the sensor hub.

The sensor hub collects data from all connected sensors and transmits it to the data sender module.
"""

from utils import logging
logger = logging.getLogger(__name__)


class SourceAndSink:
    """
    Class which implements the sink for the sensors.

    Data collected from all sensors will be gathered here, organized and sent
    to the data sender class.
    """

    def __init__(self, type_sensors: list, senders: list) -> None:
        self.__sensors = type_sensors
        self.__senders = senders

    def sink(self) -> list:
        """Collect all the data from all the found sensors."""
        logger.debug("Collecting data ...")
        collected = []

        for type_sensor in self.__sensors:
            data = type_sensor.get_payload()
            collected.append(data)

        return collected
