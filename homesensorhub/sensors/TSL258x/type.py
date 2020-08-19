from sensors.sensor_types import Light


class TSL258xType:

    SENSOR_NAME = 'TSL258x'

    def __init__(self, sensor):
        """Initialise the TSL258x type with the physical sensor."""
        self._sensor = sensor

    def get_sensor_name(self):
        return self.SENSOR_NAME

    def get_sensor_value(self):
        raise NotImplementedError("The value read for this sensor must be implemented.")

    def get_sensor_measure(self):
        """Return the measurement unit for the sensor."""
        raise NotImplementedError("The measurement unit must be implemented by the child sensor.")


class LightTSL258x(TSL258xType, Light):
    MEASURE = 'Lux'

    def __init__(self, sensor):
        TSL258xType.__init__(self, sensor)
        Light.__init__(self)

    def get_sensor_value(self) -> int:
        return self._sensor.read()

    def get_sensor_measure(self) -> str:
        return LightTSL258x.MEASURE
