"""
Module which implements the sensor hub.

The sensor hub collects data from all connected sensors and transmits it to the
data sender module.
"""
import logging
import time

from communication.data_sender import DataSender
from sensors.environmental_sensor import EnvironmentalSensorProbe
from sensors.light_sensor import LightSensorProbe

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

    def __init__(self) -> None:
        """
        Initialise the necessary objects for sinking collected data.

        Each sensor will have an entry in the data directory.

        :return: None
        """
        self.data = {}

        self.environmental_sensors = EnvironmentalSensorProbe()
        self.light_sensors = LightSensorProbe()

        self.all_sensors = [self.environmental_sensors,
                            self.light_sensors]
        # TODO use getattr to iterate only over the sensors instead of
        # hardcoding them into a list.

    def get_data(self) -> dict:
        """
        Return the collected data.

        :return directory
        """
        return self.data

    def collect_data_from(self, sensor_type) -> None:
        """
        Collect data from a specified sensor.

        Since all of the types (eg. environmental, motion, light) can have
        multiple sensors, over a call we get the data from all the selected
        type's sensors (for now).

        :return: None
        """
        for sensor in sensor_type.get_sensors():
            data = sensor.get_data()
            self.data.update(data)

    def sink(self) -> None:
        """
        Collect all the data from all the sensors.

        :return: None
        """
        # TODO Fix the multiple sensors data. When a sensor type has multiple
        # sensors, it actually overwrites the last value rather than having
        # different values for different sensors
        logging.debug("Collecting and sinking all data.")
        for sensor in self.all_sensors:
            self.collect_data_from(sensor)

    def sink_and_send(self, interval) -> None:
        """
        Sink all data from the sensors and send at a specified time interval.

        :return: None
        """
        logging.info("Sinking and sending data.")
        sender = DataSender()

        while True:
            self.sink()
            sender.send_data(self.data)
            time.sleep(interval)
