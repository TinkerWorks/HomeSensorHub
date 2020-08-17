"""Module which implements the Bosch280BME pressure sensor module logic."""
from sensors.types.pressure import Pressure


class PressureBoschBME280(Pressure):
    """Class which implements the pressure paired with AdafruitBME280."""

    MEASURE = 'Celsius'
    SENSOR_NAME = 'BoschBME280'

    def __init__(self, sensor):
        """
        Initialise the pressure.

        The object is initialised with the physical sensor responsable for providing values of this
        type. As an example, the name can be "BoschBME280".
        """
        self.__sensor = sensor

    def get_sensor_name(self) -> str:
        """
        Return the actual name of the sensor (eg. BME280, BME680 etc.).

        :return: string
        """
        return self.SENSOR_NAME

    def get_sensor_value(self) -> float:
        """
        Return the value collected by the sensor.

        :return: float
        """
        return self.__sensor.pressure

    def get_sensor_measure(self) -> str:
        """
        Return the unit of measurement for the pressure for this sensor module.

        :return: string
        """
        return PressureBoschBME280.MEASURE
