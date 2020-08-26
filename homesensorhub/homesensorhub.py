"""Entry point for the application."""
from routing.sensor_sink import SourceAndSink
from routing.mqtt_sender import MQTTSender
from routing.mqtt_subscriber import MQTTSubscriber

from sensors.BoschBME280.probe import ProbeBoschBME280
from sensors.BoschBME680.probe import ProbeBoschBME680
from sensors.TSL258x.probe import ProbeTSL258x
from sensors.RCWL0515.probe import ProbeRCWL0515


class HomeSensorHub:
    def __init__(self):
        self.__mqtt_subscriber = MQTTSubscriber()

        probe_functions = self.find_probe_functions()
        self.__senders = self.find_senders()
        self.__sensors = self.find_sensors(probe_functions)

        self.__mqtt_subscriber.subscribe_to_sensor_properties(self.__sensors)

    def run(self):
        sensor_sink = SourceAndSink(self.__sensors, self.__senders)
        sensor_sink.sink_and_send()

    def find_probe_functions(self):
        probe_functions = []

        probe_functions.append(ProbeBoschBME280.probe)
        probe_functions.append(ProbeBoschBME680.probe)
        probe_functions.append(ProbeTSL258x.probe)
        probe_functions.append(ProbeRCWL0515.probe)

        return probe_functions

    def find_senders(self):
        senders = []

        senders.append(MQTTSender())

        return senders

    def find_sensors(self, probe_functions):
        sensors = []
        mqtt_sender = self.__senders[0]

        for function in probe_functions:
            sensor_list = function(mqtt_sender.send_payload)  # TODO: Send a generic sender callback. # noqa
            try:
                sensors += sensor_list
            except TypeError:
                pass

        return sensors
