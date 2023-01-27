from homesensorhub.routing.mqtt import MQTT

from homesensorhub.utils import logging
logger = logging.getLogger(__name__)


class MQTTSubscriber():
    """Implement MQTT subscribe for on the fly config."""

    def __init__(self, broker_url="mqtt.tinker.haus", broker_port=1883):
        self.__mqtt = MQTT(broker_url, broker_port)
        self.__topics = []
        self.__mqtt.set_message_callback(self.__on_message)
        self.__sensors = None

    def subscribe_to_sensor_properties(self, sensors: list) -> None:
        """Subscribe the sensors to the topics.

        Args:
            sensors (list): The connected sensors.
        """
        self.__set_sensors(sensors)
        self.set_sensors_subscribe_topics()
        self.__mqtt.subscribe(self.__topics)

    def __set_sensors(self, sensors):
        """Set sensors for topic set and message callbacks."""
        self.__sensors = sensors

    def __on_message(self, client, userdata, message):
        # pylint: disable=unused-argument
        """Read message and set property based on the type and payload."""
        logger.debug(f"Topic {message.topic}.\n Payload {message.payload}")
        sensor_type, sensor_property = self.get_type_and_property(message.topic)

        for sensor in self.__sensors:
            if sensor.get_type() == sensor_type:
                self.set_property(sensor, sensor_property, message.payload)

    def set_property(self, sensor, sensor_property, payload):
        """Call the setter of the sensor for the property with the read payload."""
        sensor_properties = sensor.get_properties()

        for sp in sensor_properties:
            if sp == sensor_property:
                sensor_properties[sp].setter(payload)

    def get_type_and_property(self, topic) -> tuple:
        """Split the topic to extract the type and property."""
        baseless_topic = topic.replace(self.__mqtt.get_topic_base(), '')
        split_topic = baseless_topic.split(sep='/')
        sensor_type = split_topic[1]
        sensor_property = split_topic[2]

        return sensor_type, sensor_property

    def set_sensors_subscribe_topics(self):
        """Extract type and propetries from each sensor and build their subscribe topics."""
        for sensor in self.__sensors:
            sensor_type = sensor.get_type()
            self.__set_sensor_subscribe_topic(sensor_type=sensor_type,
                                              sensor_properties=sensor.get_properties())

        logger.info("Generated subscribed topics:")
        for topic in self.__topics:
            logger.info(f"    {topic}")

    def __set_sensor_subscribe_topic(self, sensor_type, sensor_properties):
        """
        Build a sensor's subscribe topic based on its properties and type.

        One topic will have the following structure:
        /developer/hostname/sensor_type/property
        /babycakes/sensors-office/temperature/pollrate

        By calling mqtt publish for one of the sensor's build topics, one can send messages as
        follows:
        /user/hostname/sensor_type/property 10
        """
        for sensor_property in sensor_properties.keys():
            type_topic = "/" + sensor_type
            property_topic = "/" + sensor_property
            topic = f"{self.__mqtt.get_topic_base()}{type_topic}{property_topic}"
            self.__topics.append((topic, self.__mqtt.get_qos()))
