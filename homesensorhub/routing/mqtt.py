import paho.mqtt.client as mqtt
import socket
import os
import getpass
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MQTT(metaclass=Singleton):
    def __init__(self, broker_url="mqtt.tinker.haus", broker_port=1883):
        self.__client = mqtt.Client()
        self.__broker_url = broker_url
        self.__broker_port = broker_port

        self.__host = socket.gethostname() + "/"
        self.__dev = getpass.getuser() + "/"
        if os.getuid() == 0:
            self.__dev = ""
        self.__topic_base = self.__dev + self.__host

        self.connect()
        print(self)

    def connect(self, retry=5):
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

    def get_topic_base(self):
        return self.__topic_base

    def get_client(self):
        return self.__client
