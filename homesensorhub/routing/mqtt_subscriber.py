from routing.mqtt import MQTT

import logging


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class MQTTSubscriber():
    """Implement MQTT subscribe for on the fly config."""

    def __init__(self, broker_url="mqtt.tinker.haus", broker_port=1883):
        self.__mqtt = MQTT(broker_url, broker_port)
        self.__topics = []

    def set_sensors_subscribe(self, sensors: list):
        for sensor in sensors:
            type = sensor.get_type()
            self.set_sensor_subscribe(type=type, sensor_properties=sensor.get_properties())
        print("Generated topics: {}".format(self.__topics))

    def set_sensor_subscribe(self, type, sensor_properties):
        for property in sensor_properties.keys():
            property_topic = property + "/"
            type_topic = type + "/"

            topic = "{}{}{}".format(self.__mqtt.get_topic_base(), type_topic, property_topic)
            # from https://pypi.org/project/paho-mqtt/#subscribe-unsubscribe, both the topic and
            # the qos are necessary to be present in the subscribe touple;
            self.__topics.append(topic)

    def subscribe(self):
        client = self.__mqtt.get_client()
        client.loop_stop()
        client.subscribe(self.__topics)
        client.loop_start()
