"""
Module which implements the sensor hub.

The sensor hub collects data from all connected sensors and transmits it to the
data sender module.
"""
import logging
import time

from routing.mqtt_sender import MQTTDataSender

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class SourceAndSink:
    """
    Class which implements the sink for the sensors.

    Data collected from all sensors will be gathered here, organized and sent
    to the data sender class.
    """

    def __init__(self, type_sensors, senders) -> None:
        """
        Initialise the necessary objects for sinking collected data.

        Each sensor will have an entry in the data directory.

        :return: None
        """
        self.__sensors = type_sensors
        self.__senders = senders

    def sink(self) -> None:
        """
        Collect all the data from all the sensors.

        For each type (environmental, light and motion for now) we request data
        from their attached sensors.

        :return: None
        """
        logging.debug("Started sinking...")
        collected = []

        for type_sensor in self.__sensors:
            data = type_sensor.get_payload()
            collected.append(data)

        return collected

    def sink_and_send(self, interval) -> None:
        """
        Sink all data from the sensors and send at a specified time interval.

        :return: None
        """
        logging.info("Sinking and sending data.")
        sender = MQTTDataSender()

        while True:
            collected = self.sink()
            sender.send(collected)
            time.sleep(interval)
