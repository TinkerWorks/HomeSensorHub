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
        self.__mqtt.get_client().on_message = self.on_message
        self.__sensors = None

    def set_sensors(self, sensors):
        """Set sensors for topic set and message callbacks."""
        self.__sensors = sensors

    def on_message(self, client, userdata, message):
        print("{};".format(dir(message)))

    def set_sensors_subscribe_topics(self):
        """Extract type and propetries from each sensor and build their subscribe topics."""
        for sensor in self.__sensors:
            type = sensor.get_type()
            self.__set_sensor_subscribe_topic(type=type, sensor_properties=sensor.get_properties())

        print("Generated topics: {}".format(self.__topics))

    def __set_sensor_subscribe_topic(self, type, sensor_properties):
        """
        Build a sensor's subscribe topic based on its properties and type.

        One topic will have the following structure:
        /developer/hostname/sensor_type/property
        /babycakes/sensors-office/temperature/pollrate

        By calling mqtt publish for one of the sensor's build topics, one can send messages as
        follows:
        /developer/hostname/sensor_type/property 10
        """
        for property in sensor_properties.keys():
            property_topic = property + "/"
            type_topic = type + "/"
            topic = "{}{}{}".format(self.__mqtt.get_topic_base(), type_topic, property_topic)

            self.__topics.append((topic, self.__mqtt.get_qos()))

    def subscribe(self):
        """Stop the mqtt subscribe loop to add the sensors properties subscribe topics."""
        client = self.__mqtt.get_client()
        client.loop_stop()

        logging.info("Setting MQTT subscribers.")
        client.subscribe(self.__topics)

        client.loop_start()
