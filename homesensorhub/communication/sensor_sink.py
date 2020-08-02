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
        self.environmental_probe = EnvironmentalSensorProbe()
        self.light_probe = LightSensorProbe()

        self.probes = [self.environmental_probe,
                       self.light_probe]

    def sink(self) -> dict:
        """
        Collect all the data from all the sensors.

        :return: None
        """
        # TODO Fix the multiple sensors data. When a sensor type has multiple
        # sensors, it actually overwrites the last value rather than having
        # different values for different sensors
        logging.debug("Collecting and sinking all data.")

        sinked_data = {}

        for probe in self.probes:
            for sensor in probe.get_sensors():
                data = sensor.collect_data()
                sinked_data.update(data)

        return sinked_data

    def sink_and_send(self, interval) -> None:
        """
        Sink all data from the sensors and send at a specified time interval.

        :return: None
        """
        logging.info("Sinking and sending data.")
        sender = DataSender()

        while True:
            sinked_data = self.sink()
            sender.send_data_to_mqtt(sinked_data)
            time.sleep(interval)
