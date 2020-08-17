"""Module which implements the Bosch280BME altitude sensor module set up."""
from sensors.types.altitude import Altitude


class AltitudeBoschBME280(Altitude):
    """Class which implements the altitude collected from BoschBME280 sensor module."""

    MEASURE = 'Meters'
    SENSOR_NAME = 'BoschBME280'

    def __init__(self, sensor, sensor_name):
        self.__sensor = sensor
        self.__sensor_name = sensor_name

    def get_sensor_name(self) -> str:
        """
        Return the actual name of the sensor (eg. BME280, BME680 etc.).

        :return: string
        """
        return self.__sensor_name

    def get_sensor_value(self) -> int:
        """
        Return the value collected by the sensor.

        :return: int
        """
        return self.__sensor.altitude

    def get_sensor_measure(self) -> str:
        """
        Return the unit of measurement for the altitude for this sensor module.

        :return: string
        """
        return AltitudeBoschBME280.MEASURE
