from routing.mqtt import MQTT

import logging


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')


class MQTTSubscriber():
    """Implement MQTT subscribe for on the fly config."""

    def __init__(self, broker_url="mqtt.tinker.haus", broker_port=1883):
        self.__mqtt = MQTT(broker_url, broker_port)
        self.__topics = []
        self.__mqtt.get_client().on_message = self.on_message
        self.__mqtt.get_client().on_log = self.on_log
        self.__sensors = None

    def set_sensors(self, sensors):
        """Set sensors for topic set and message callbacks."""
        self.__sensors = sensors

    def on_log(self, mqttc, obj, level, string):
        logging.debug(string)

    def on_message(self, client, userdata, message):
        """Read message and set property based on the type and payload."""
        type, property = self.get_type_and_property(message.topic)

        for sensor in self.__sensors:
            if sensor.get_type() == type:
                self.set_property(sensor, property, message.payload)

    def set_property(self, sensor, property, payload):
        """Call the setter of the sensor for the property with the read payload."""
        sensor_properties = sensor.get_properties()

        for sp in sensor_properties:
            if sp == property:
                sensor_properties[sp].setter(payload)

    def get_type_and_property(self, topic) -> tuple:
        """Split the topic to extract the type and property."""
        baseless_topic = topic.replace(self.__mqtt.get_topic_base(), '')
        split_topic = baseless_topic.split(sep='/')
        type = split_topic[0]
        property = split_topic[1]

        return type, property

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
            type_topic = type + "/"
            topic = "{}{}{}".format(self.__mqtt.get_topic_base(), type_topic, property)
            self.__topics.append((topic, self.__mqtt.get_qos()))

    def subscribe(self):
        """Stop the mqtt subscribe loop to add the sensors properties subscribe topics."""
        client = self.__mqtt.get_client()
        client.loop_stop()

        logging.info("Setting MQTT subscribers.")
        client.subscribe(self.__topics)

        client.loop_start()
