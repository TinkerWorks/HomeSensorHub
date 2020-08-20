from routing.mqtt import MQTT

import logging


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class MQTTSubscriber:
    """Implement MQTT subscribe for on the fly config."""

    def __init__(self, broker_url="mqtt.tinker.haus", broker_port=1883):
        self.__mqtt = MQTT(broker_url, broker_port)
        self.subscribe()

    def subscribe(self):
        client = self.__mqtt.get_client()
        client.loop_stop()
        client.subscribe("min")
        client.loop_start()
