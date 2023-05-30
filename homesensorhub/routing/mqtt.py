import paho.mqtt.client as mqtt
import socket
import os
import getpass
import time

from homesensorhub.utils import logging
from homesensorhub.utils.configuration import Configuration
logger = logging.getLogger(__name__)


class Singleton(type):
    """Generic singleton pattern for classes."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MQTT(metaclass=Singleton):
    """Create and hold connection through MQTT."""
    QOS = 0

    def __init__(self):
        self.__client = mqtt.Client()
        self.__client.enable_logger()
        self.__client.on_connect = self.on_connect

        Configuration().set_callback_update('mqtt', self.update_connection)
        self.__broker_url = Configuration().entry('mqtt', 'address',
                                                  default_entry_value="mqtt.tinker.haus")
        self.__broker_port = Configuration().entry('mqtt', 'port',
                                                   default_entry_value=1883)
        self.__hostname = socket.gethostname()
        self.__dev = getpass.getuser() + "/"
        if os.getuid() == 0:
            self.__dev = ""
        self.__topic_base = self.__dev + self.__hostname

        self.connect()

    def update_connection(self, entry_name: str):
        """Update the values of the broker url and port with data from the configuration file."""
        # TODO set timer
        logger.debug("Update connection MQTT")
        self.__broker_url = Configuration().entry('mqtt', 'address',
                                                  default_entry_value="mqtt.tinker.haus")
        self.__broker_port = Configuration().entry('mqtt', 'port',
                                                   default_entry_value=1883)
        try:
            self.__client.loop_stop()
            self.connect()
        except socket.gaierror as error:
            logger.error(error)

    def connect(self):
        """Connect to the MQTT server."""
        logger.info("Trying to connect to %s:%s...", self.__broker_url, self.__broker_port)
        # connect_async has to be used instead of connect
        # otherwise it will not reconnect on server reboot
        try:
            self.__client.connect_async(self.__broker_url,
                                        self.__broker_port)
            self.__client.loop_start()
        except ValueError as error:
            logger.error("MQTT connection failed to %s:%s.", self.__broker_url, self.__broker_port)
            logger.error(error)

    def set_message_callback(self, callback):
        self.__client.on_message = callback

    def subscribe(self, topics):
        """Stop the mqtt subscribe loop to add the sensors properties subscribe topics."""
        self.__client.loop_stop()

        logger.info("Setting MQTT subscribers.")
        self.__client.subscribe(topics)

        self.__client.loop_start()

    def publish(self, topic, payload):
        result = (mqtt.MQTT_ERR_AGAIN, 0)

        while result[0] != mqtt.MQTT_ERR_SUCCESS:
            result = self.__client.publish(topic=topic,
                                           payload=payload,
                                           qos=0,
                                           retain=False)

            if (result[0] == mqtt.MQTT_ERR_NO_CONN):
                logger.warning("MQTT bus unresponsive, reconnecting...")
                self.connect()
                time.sleep(1)

    def on_connect(self, client, userdata, flags, rc):
        logger.info("MQTT connect callback called with rc = %s", rc)

    def get_topic_base(self):
        """Return topic base used for publish."""
        return self.__topic_base

    def get_qos(self):
        return MQTT.QOS

