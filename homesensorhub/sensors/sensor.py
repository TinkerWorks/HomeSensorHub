"""Module which implements a basic sensor."""


class Sensor:
    """Class which implements a basic sensor functionality."""

    def __init__(self, sensor, name):
        """
        Initialise the ingredients for a basic sensor skeleton.

        Each sensor has a name and data which will be collected.
        The name of the sensor represents the physical name (such as bme280).
        Each sensor will be detected by probing by each type (light, motion,
        environment).
        """
        self.__sensor = sensor
        self.__name = name

    def get_data(self):
        """
        Collect the data from each sensor type.

        Each type may have multiple values collected (such as temperature,
        altitude, pressure and humidity for the environmental one).
        """
        pass

    def get_sensor_name(self) -> str:
        """
        Return the actual name of the sensor (eg. BME280, BME680 etc.).

        :return: string
        """
        return self.__name

    def get_sensor(self):
        """Return the physical sensor attached to this object."""
        return self.__sensor
