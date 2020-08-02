
"""Module which implements the classes for sending collected data to MQTT."""
from . import payload as p

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
        """
        Send the collected sensor data to mqtt.

        The topic represents the type of the sensor. The data paremeter will be
        of the form:

        {'temperature':
            {
            'type': 'temperature',
             'name': <class 'adafruit_bme280.Adafruit_BME280_I2C'>,
             'value': 28.0955078125,
             'timestamp': datetime.datetime(2020, 8, 2, 22, 18, 1, 744014),
             'measurement': 'celsius'
             }
        }

        The topic is collected from the outer most key of the dictionary, in
        this case, 'temperature'. The packet represents the colleced data from
        this type of sensor.
        """
        for topic, packet in data.items():
            self.send_current_to_mqtt(topic, packet)

    def send_current_to_mqtt(self, topic, packet):
        """
        Send the current packet of information collected by the sensors.

        For now only the "current" topic is implemented. Others as "goal" will
        also be set in place.
        """
        topic = "{}/{}/current".format(self.__host, topic)
        payload = p.Payload(packet)
        result = (mqtt.MQTT_ERR_AGAIN, 0)

        while result[0] != mqtt.MQTT_ERR_SUCCESS:
            result = self.client.publish(topic=topic,
                                         payload=payload.get_mqtt_payload(),
                                         qos=0,
                                         retain=False)

            if(result[0] == mqtt.MQTT_ERR_NO_CONN):
                logging.warn("MQTT bus unresponsive, trying to reconnect ...")
                self.connect()
                time.sleep(1)
