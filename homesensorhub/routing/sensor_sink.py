"""
Module which implements the sensor hub.

The sensor hub collects data from all connected sensors and transmits it to the data sender module.
"""
import logging
import threading
from signal import signal, SIGINT, SIGTERM

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

    running = True

    def __init__(self, type_sensors: list, senders: list) -> None:
        self.__sensors = type_sensors
        self.__senders = senders

    def sink(self) -> list:
        """Collect all the data from all the found sensors."""
        logging.debug("Collecting data ...")
        collected = []

        for type_sensor in self.__sensors:
            data = type_sensor.get_payload()
            collected.append(data)

        return collected

    def sink_and_send(self) -> None:
        """Sink all data from the sensors and send at a specified time interval."""
        logging.info("Sinking and sending data...")

        self.event = threading.Event()

        signal(SIGINT, self.stop_everything)
        signal(SIGTERM, self.stop_everything)

        self.event.wait()

        print("Quitting gracefully")
        for sensor in self.__sensors:
            sensor.stop()

    def stop_everything(self, signal_received, frame) -> None:
        print("stop caught")
        self.event.set()
        SourceAndSink.running = False
