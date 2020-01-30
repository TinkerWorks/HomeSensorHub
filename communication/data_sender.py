import time

import paho.mqtt.client as mqtt
import socket


class DataSender:
    HOST = "unknown"

    TEMPERATURE_TOPIC = "temperature"
    HUMIDITY_TOPIC = "humidity"

    def __init__(self, broker_url="mqtt", broker_port=1883):
        self.client = mqtt.Client()
        self.client.connect(broker_url, broker_port)

        self.HOST = socket.gethostname()

    def send_data(self, data):
        for topic, value in data.items():
            self.send_current(value, topic)

    def send_current(self, value, topic):
        topic = self.HOST + "/" + topic + "/current"
        pld = f'{value:.3f}'
        self.client.publish(topic=topic, payload=pld, qos=0, retain=False)

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
