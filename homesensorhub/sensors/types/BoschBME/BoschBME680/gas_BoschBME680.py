"""Module which implements the Bosch680BME gas sensor module set up."""
from sensors.types.gas import Gas


class GasBoschBME680(Gas):
    """Class which implements the gas collected from BoschBME680 sensor module."""

    MEASURE = 'Meters'
    SENSOR_NAME = 'BoschBME680'

    def __init__(self, sensor, sensor_name):
        self.__sensor = sensor
        self.__sensor_name = sensor_name

    def get_sensor_name(self) -> str:
        """
        Return the actual name of the sensor (eg. BME680, BME680 etc.).

        :return: string
        """
        return self.__sensor_name

    def get_sensor_value(self) -> int:
        """
        Return the value collected by the sensor.

        :return: int
        """
        return self.__sensor.gas

    def get_sensor_measure(self) -> str:
        """
        Return the unit of measurement for the gas for this sensor module.

        :return: string
        """
        return GasBoschBME680.MEASURE
