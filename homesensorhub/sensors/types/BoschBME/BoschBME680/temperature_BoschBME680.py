"""Module which implements the Bosch680BME temperature sensor module logic."""
from sensors.types.sensor_type import Temperature


class TemperatureBoschBME680(Temperature):
    """Class which implements the temperature paired with AdafruitBME680."""

    MEASURE = 'Celsius'
    SENSOR_NAME = 'BoschBME680'

    def __init__(self, sensor):
        """
        Initialise the temperature.

        The object is initialised with the physical sensor responsable for providing values of this
        type. As an example, the name can be "BoschBME680".
        """
        self.__sensor = sensor

    def get_sensor_name(self) -> str:
        """
        Return the actual name of the sensor (eg. BME680, BME680 etc.).

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
        return TemperatureBoschBME680.MEASURE
