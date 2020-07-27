import logging
import time
import paho.mqtt.client as mqtt
import socket

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class DataSender:
    HOST = "unknown"

    TEMPERATURE_TOPIC = "temperature"
    HUMIDITY_TOPIC = "humidity"

    def __init__(self, broker_url="mqtt.tinker.haus", broker_port=1883):
        self.client = mqtt.Client()

        self.broker_url_ = broker_url
        self.broker_port_ = broker_port
        self.HOST = socket.gethostname()

        self.client.enable_logger(logging)

        self.connect()

    def connect(self, retry = 5):
        while (retry > 0):
            try:
                cnct = self.client.connect(self.broker_url_, self.broker_port_)
                logging.debug("connect result: " + str(cnct))
                if cnct == 0:
                    return True

            except ConnectionRefusedError as e:
                logging.error("connect refused: " + str(e))

            retry-=1


        return False

    def send_data(self, data):
        for topic, value in data.items():
            self.send_current(value, topic)

    def send_current(self, value, topic):
        topic = self.HOST + "/" + topic + "/current"
        payload = value #TODO: This give us invalid syntax: f'{value:.3f}'
        logging.info("Sending data to :" + topic + " --> " + str(payload))

        result = (mqtt.MQTT_ERR_AGAIN,0)
        while result[0] != mqtt.MQTT_ERR_SUCCESS:
            result = self.client.publish(topic=topic, payload=payload, qos=0, retain=False)

            if(result[0] == mqtt.MQTT_ERR_NO_CONN):
                logging.warn("MQTT bus unresponsive, trying to reconnect ...")
                self.connect()
                time.sleep(1)



    def send_temperature(self, value):
        self.send_current(value, self.TEMPERATURE_TOPIC)

    def send_humidity(self, value):
        self.send_current(value, self.HUMIDITY_TOPIC)


if __name__ == "__main__":
    from time import sleep
    ds = DataSender()
    temp = 3.14

    while True:
        sleep(1)
        ds.send_temperature(temp)
        ds.send_humidity(temp * 2)
        temp += 0.2
