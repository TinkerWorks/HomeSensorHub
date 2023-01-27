"""Entry point for the application."""

import sys

from threading import Event
from signal import signal, SIGINT, SIGTERM

from homesensorhub.flask_data.flask_application import FlaskApp

from homesensorhub.routing.mqtt_sender import MQTTSender
from homesensorhub.routing.mqtt_subscriber import MQTTSubscriber

try:
    from homesensorhub.sensors.BoschBME.BoschBME280.probe import ProbeBoschBME280
    from homesensorhub.sensors.BoschBME.BoschBME680.probe import ProbeBoschBME680
    from homesensorhub.sensors.TSL258x.probe import ProbeTSL258x
    from homesensorhub.sensors.RCWL0515.probe import ProbeRCWL0515
except NotImplementedError:
    print("Running on PC.")

from homesensorhub.utils import logging
logger = logging.getLogger(__name__)

print(sys.path)


class HomeSensorHub:
    """Configures and runs the homesensorhub module.

    Starts the MQTT bus and configures the connected sensors.
    """
    def __init__(self):
        logger.success("Starting HomeSensorHub ...")
        self.__initialize_stop()  # initialize stop here so we are prepared

        self.__flask_application = FlaskApp()

        self.__mqtt_subscriber = MQTTSubscriber()

        probe_functions = self.__find_probe_functions()
        self.__senders = self.__find_senders()
        self.__sensors = self.__find_sensors(probe_functions)

        self.__mqtt_subscriber.subscribe_to_sensor_properties(self.__sensors)

    def run(self):
        """Start the homesensorhub application."""
        self.__flask_application.run()
        logger.success("Running HomeSensorHub ...")

        # just wait for the stop event
        self.event.wait()
        logger.notice("QUIT signal received !")
        for sensor in self.__sensors:
            sensor.stop()

        logger.notice("Quitting gracefully !")

    def __initialize_stop(self):
        self.event = Event()
        signal(SIGINT, self.__stop_everything)
        signal(SIGTERM, self.__stop_everything)

    def __stop_everything(self, signal_received, frame) -> None:
        # pylint: disable=unused-argument
        self.event.set()

    def __find_probe_functions(self):
        probe_functions = []

        probe_functions.append(ProbeBoschBME280.probe)
        probe_functions.append(ProbeBoschBME680.probe)
        probe_functions.append(ProbeTSL258x.probe)
        probe_functions.append(ProbeRCWL0515.probe)

        return probe_functions

    def __find_senders(self):
        senders = []

        logger.info("Configuring senders ...")
        senders.append(MQTTSender())

        return senders

    def __find_sensors(self, probe_functions):
        sensors = []
        mqtt_sender = self.__senders[0]

        logger.info("Searching attached sensors ...")
        for function in probe_functions:
            sensor_list = function(mqtt_sender.send_payload) # TODO: Send a generic sender callback. # noqa # pylint: disable=fixme
            try:
                sensor_list = function(mqtt_sender.send_payload)  # TODO: Send a generic sender callback. # noqa
                sensors += sensor_list
            except Exception as e:
                logger.error(e)

        return sensors


def main():
    """Sets up the main homesensorhub application, as well as the Flask one."""
    homesensorhub = HomeSensorHub()
    homesensorhub.run()


if __name__ == "__main__":
    main()
