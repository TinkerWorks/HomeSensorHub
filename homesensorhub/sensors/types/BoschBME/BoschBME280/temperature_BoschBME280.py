"""Module which implements the Bosch280BME temperature sensor module logic."""
from sensors.types.temperature import Temperature


class TemperatureBoschBME280(Temperature):
    """Class which implements the temperature paired with AdafruitBME280."""

    MEASURE = 'Celsius'
    SENSOR_NAME = 'BoschBME280'

    def __init__(self, sensor):
        """
        Initialise the temperature.

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
        return self.__sensor.temperature

    def get_sensor_measure(self) -> str:
        """
        Return the unit of measurement for the temperature for this sensor module.

        :return: string
        """
        return TemperatureBoschBME280.MEASURE
