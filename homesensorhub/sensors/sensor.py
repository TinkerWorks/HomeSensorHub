"""Module which implements a basic sensor."""


class Sensor:
    """Class which implements a basic sensor functionality."""

    def __init__(self, sensor, name):
        """
        Initialise the ingredients for a basic sensor skeleton.

        Each sensor has a name and data which will be collected. Each sensor
        will be detected by probing by each type (light, motion, environment).
        """
        self.__sensor = sensor
        self.__name = name

    def build_sensor_packet(self, type, value, timestamp, measurement):
        """Build a packet with information taken from each sensor."""
        print(self.__name)

        packet = {
            'type': type,
            'name': self.__name,
            'value': value,
            'timestamp': timestamp,
            'measurement': measurement
        }

        return packet

    def get_sensor_name(self) -> str:
        """
        Return the actual name of the sensor (eg. BME280, BME680 etc.).

        :return: string
        """
        return self.__name

    def get_sensor(self):
        """Return the physical sensor attached to this object."""
        return self.__sensor
