from routing.mqtt import MQTT

import logging


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class MQTTSubscriber:
    """Implement MQTT subscribe for on the fly config."""

    def __init__(self, broker_url="mqtt.tinker.haus", broker_port=1883):
        self.__mqtt = MQTT(broker_url, broker_port)
        self.__topics = []
        self.__qos = 0

        self.subscribe()

    def set_sensors_subscribe(self, sensors_properties: list):
        for sensor_properties in sensors_properties:
            self.set_sensor_subscribe(sensor_properties)
        print("Generated topics are: {}".format(self.__topics))

    def set_sensor_subscribe(self, sensor_properties):
        for property in sensor_properties.keys():
            property = property + "/"
            topic = "{}{}".format(self.get_topic_base(), property)
            # from https://pypi.org/project/paho-mqtt/#subscribe-unsubscribe, both the topic and
            # the qos are necessary to be present in the subscribe touple;
            self.__topics.append((topic, self.__qos))

    def subscribe(self):
        client = self.__mqtt.get_client()
        client.loop_stop()
        client.subscribe(self.__topics)
        client.loop_start()
