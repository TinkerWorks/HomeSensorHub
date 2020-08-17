"""Module which implements the Bosch280BME temperature sensor module logic."""
from sensors.types.temperature import Temperature


class TemperatureAdafruitBME280(Temperature):
    """Class which implements the temperature paired with AdafruitBME280."""

    MEASURE = 'Celsius'
    SENSOR_NAME = 'BoschBME280'

    def __init__(self, sensor, sensor_name):
        """
        Initialise the temperature.

        The object could be initialised with the physical sensor responsable
        for providing values of this type and its name. As an example, the name
        can be "adafruit_bme280".
        """
        self.__sensor = sensor
        self.__sensor_name = sensor_name

    def get_sensor_name(self) -> str:
        """
        Return the actual name of the sensor (eg. BME280, BME680 etc.).

        :return: string
        """
        return self.__sensor_name

    def get_sensor_value(self) -> float:
        """
        Return the value collected by the sensor.

        :return: float
        """
        return self.__sensor.temperature

    def get_physical_sensor(self):
        """Return the physical found sensor."""
        return self.___sensor
