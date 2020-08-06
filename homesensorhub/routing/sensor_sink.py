"""
Module which implements the sensor hub.

The sensor hub collects data from all connected sensors and transmits it to the
data sender module.
"""
import logging
import time

from routing.data_sender import DataSender

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class SensorSink:
    """
    Class which implements the sink for the sensors.

    Data collected from all sensors will be gathered here, organized and sent
    to the data sender class.
    """

    def __init__(self, sensors) -> None:
        """
        Initialise the necessary objects for sinking collected data.

        Each sensor will have an entry in the data directory.

        :return: None
        """
        self.__sensors = sensors
        self.__collected = []

    def sink(self) -> None:
        """
        Collect all the data from all the sensors.

        For each type (environmental, light and motion for now) we request data
        from their attached sensors.

        :return: None
        """
        logging.debug("Collecting and sinking all data.")

        for type_sensor in self.__sensors:
            for sensor in type_sensor.get_sensors():
                data = sensor.get_data()
                for payload in data:
                    self.__collected.append(payload)

    def sink_and_send(self, interval) -> None:
        """
        Sink all data from the sensors and send at a specified time interval.

        :return: None
        """
        logging.info("Sinking and sending data.")
        sender = DataSender()

        while True:
            self.sink()
            sender.send_data_to_mqtt(self.__collected)
            time.sleep(interval)
