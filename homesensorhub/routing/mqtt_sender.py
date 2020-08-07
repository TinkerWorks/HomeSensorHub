"""Module which implements data routing to MQTT."""
from routing.data_sender import DataSender

import logging
import paho.mqtt.client as mqtt
import socket
import time

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class MQTTDataSender(DataSender):
    """Class which implements data routing to MQTT."""

    def __init__(self, broker_url="mqtt.tinker.haus", broker_port=1883):
        """Set up and connect to MQTT."""
        self.__client = mqtt.Client()
        self.__broker_url = broker_url
        self.__broker_port = broker_port
        self.__host = socket.gethostname()

        self.connect()

    def connect(self, retry=5):
        """Set up the MQTT connection with the host."""
        while (retry > 0):
            try:
                connection = self.__client.connect(self.__broker_url,
                                                   self.__broker_port)
                logging.debug("MQTT connection result: {}".format(connection))
                if connection == 0:
                    return True
            except ConnectionRefusedError as error:
                logging.error("MQTT connect refused: {}".format(error))

            retry -= 1

        return False

    def send(self, data):
        """
        Send the current payload of information collected by the sensors.

        For now only the "current" topic is implemented. Others as "goal" will
        also be set in place.
        """
        for payload in data:
            json_payload = payload.get_json_payload()
            type = payload.get_type()

            topic = "{}/{}/current".format(self.__host, type)
            result = (mqtt.MQTT_ERR_AGAIN, 0)

            while result[0] != mqtt.MQTT_ERR_SUCCESS:
                result = self.__client.publish(topic=topic,
                                               payload=json_payload,
                                               qos=0,
                                               retain=False)

                if(result[0] == mqtt.MQTT_ERR_NO_CONN):
                    logging.warn("MQTT bus unresponsive, reconnecting...")
                    self.connect()
                    time.sleep(1)
