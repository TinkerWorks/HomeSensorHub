import paho.mqtt.client as mqtt
import socket
import os
import getpass
import time

from utils import logging
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

    def __init__(self, broker_url="mqtt.tinker.haus", broker_port=1883):
        self.__client = mqtt.Client()
        self.__client.enable_logger()
        self.__client.on_connect = self.on_connect

        self.__broker_url = broker_url
        self.__broker_port = broker_port

        self.__hostname = socket.gethostname()
        self.__dev = getpass.getuser() + "/"
        if os.getuid() == 0:
            self.__dev = ""
        self.__topic_base = self.__dev + self.__hostname

        self.connect()

    def connect(self):
        try:
            connection = self.__client.connect(self.__broker_url,
                                               self.__broker_port)
            if connection == 0:
                logger.success("MQTT connected succesfully to {}"
                               .format(self.__broker_url))
            else:
                logger.error("MQTT connection failed to {} with error code: {}"
                             .format(self.__broker_url, connection))

            self.__client.loop_start()
            return True
        except ConnectionRefusedError as error:
            logger.error("MQTT connect refused: {}".format(error))
            return False

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

            if(result[0] == mqtt.MQTT_ERR_NO_CONN):
                logger.warn("MQTT bus unresponsive, reconnecting...")
                self.connect()
                time.sleep(1)

    def on_connect(self, client, userdata, flags, rc):
        logger.info("MQTT connect callback called with rc = {}".format(rc))

    def get_topic_base(self):
        """Return topic base used for publish."""
        return self.__topic_base

    def get_client(self):
        return self.__client

    def get_broker_url(self):
        return self.__broker_url

    def get_qos(self):
        return MQTT.QOS
