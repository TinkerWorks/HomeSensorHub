
"""Module which implements the classes for sending collected data to MQTT."""

import logging
import time
import paho.mqtt.client as mqtt
import socket

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class DataSender:
    """Class which implements the MQTT send functionality."""

    def __init__(self, broker_url="mqtt.tinker.haus", broker_port=1883):
        """Set up and connect to MQTT."""
        self.client = mqtt.Client()

        self.__broker_url = broker_url
        self.__broker_port = broker_port
        self.__host = socket.gethostname()

        self.client.enable_logger(logging)

        self.connect_mqtt()

    def connect_mqtt(self, retry=5):
        """Set up the MQTT connection with the host."""
        while (retry > 0):
            try:
                connection = self.client.connect(self.__broker_url,
                                                 self.__broker_port)
                logging.debug("MQTT connection result: {}".format(connection))
                if connection == 0:
                    return True
            except ConnectionRefusedError as error:
                logging.error("MQTT connect refused: {}".format(error))

            retry -= 1

        return False

    def send_data_to_mqtt(self, data):
        """Send the collected sensor data to mqtt."""
        for payload in data:
            self.send_current_to_mqtt(payload)

    def send_current_to_mqtt(self, payload):
        """
        Send the current payload of information collected by the sensors.

        For now only the "current" topic is implemented. Others as "goal" will
        also be set in place.
        """
        json_payload = payload.get_json_payload()
        type = payload.get_type()

        topic = "{}/{}/current".format(self.__host, type)
        result = (mqtt.MQTT_ERR_AGAIN, 0)

        while result[0] != mqtt.MQTT_ERR_SUCCESS:
            result = self.client.publish(topic=topic,
                                         payload=json_payload,
                                         qos=0,
                                         retain=False)

            if(result[0] == mqtt.MQTT_ERR_NO_CONN):
                logging.warn("MQTT bus unresponsive, trying to reconnect ...")
                self.connect()
                time.sleep(1)
