from sensors.types.sensor_type import Light


class LightTSL258x(Light):

    MEASURE = 'Lux'
    SENSOR_NAME = 'TSL258x'

    def __init__(self, sensor):
        self.__sensor = sensor

    def get_sensor_name(self) -> str:
        """
        Return the actual name of the sensor (eg. TSL258x).

        :return: string
        """
        return LightTSL258x.SENSOR_NAME

    def get_sensor_value(self) -> float:
        """
        Return the value collected by the sensor.

        :return: float
        """
        return self.__sensor.read()

    def get_sensor_measure(self) -> str:
        """
        Return the unit of measurement for the temperature for this sensor module.

        :return: string
        """
        return LightTSL258x.MEASURE
