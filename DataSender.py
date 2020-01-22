import paho.mqtt.client as mqtt
import socket

class DataSender:
    host = "unknown"
    temperature_topic = "temperature"
    humidity_topic = "humidity"

    current_topic = "current"

    def __init__(self, broker_url = "mqtt", broker_port = 1883):
        self.client = mqtt.Client()
        self.client.connect(broker_url, broker_port)

        self.host = socket.gethostname()

    def sendCurrent(self, value, topic):
        topic = self.host + "/" + topic + "/" + self.current_topic
        pld = f'{value:.3f}'
        #pld = str(value)
        self.client.publish(topic=topic, payload=pld, qos=0, retain=False)


    def sendTemperature(self, value):
        self.sendCurrent(value, self.temperature_topic)

    def sendHumidity(self, value):
        self.sendCurrent(value, self.humidity_topic)


if __name__ == "__main__":
    from time import sleep
    ds = DataSender()
    temp = 3.14

    while True:
        sleep(1)
        ds.sendTemperature (temp)
        ds.sendHumidity (temp * 2)
        temp += 0.2
