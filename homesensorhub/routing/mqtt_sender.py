"""Module which implements data routing to MQTT."""
from routing.data_sender import DataSender
from routing.mqtt import MQTT

import logging
import paho.mqtt.client as mqtt
import time

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class MQTTSender(DataSender):
    """Implement data routing to MQTT."""

    def __init__(self, broker_url="mqtt.tinker.haus", broker_port=1883):
        self.__mqtt = MQTT(broker_url, broker_port)

    def send(self, data):
        """
        Send all collected data to MQTT.

        This sends the json payload, as well as simple values.
        """
        for payload in data:
            self.send_payload(payload)

    def send_payload(self, payload):
        self.__send_json_payload(payload)
        self.__send_simple_values(payload)

    def __send_json_payload(self, payload):
        """
        Send the current payload of information collected by the sensors.

        This contains the payload with all its gained information, of the
        following form:

        sensors-office/temperature/current {
            "measurement" = "celsius".
            "name" = "<class 'adafruit_bme280.Adafruit_BME280_I2C'>".
            "timestamp" = "2020-08-07 15:28:40.180167".
            "type" = "temperature".
            "value" = "27.28"
        }
        """
        json_payload = payload.get_json_payload()
        type = payload.get_str_type() + "/"
        topic_base = self.__mqtt.get_topic_base()
        topic = "{}{}current".format(topic_base, type)

        self.__publish(topic, json_payload)

    def __send_simple_values(self, payload):
        """
        Send simple collected values to MQTT.

        Each publish contains the type of the sensor, what type of attribute of
        the payload it represents and its value, as the following example:

        sensors-office/temperature/current/value 27.68
        """
        payload_attributes = payload.get_string_payload()

        for attribute, collected in payload_attributes.items():
            type = payload.get_str_type() + "/"
            topic_base = self.__mqtt.get_topic_base()
            topic = "{}{}current/{}".format(topic_base, type, attribute)

            self.__publish(topic, collected)

    def __publish(self, topic, payload):
        result = (mqtt.MQTT_ERR_AGAIN, 0)

        while result[0] != mqtt.MQTT_ERR_SUCCESS:
            mqtt_client = self.__mqtt.get_client()
            result = mqtt_client.publish(topic=topic,
                                         payload=payload,
                                         qos=0,
                                         retain=False)

            if(result[0] == mqtt.MQTT_ERR_NO_CONN):
                logging.warn("MQTT bus unresponsive, reconnecting...")
                self.connect()
                time.sleep(1)
