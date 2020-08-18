from sensors.sensor_types import Humidity, Pressure, Altitude, Temperature, Gas


class BoschBME680Type:

    SENSOR_NAME = 'BoschBME680'

    def __init__(self, sensor):
        """Initialise the BoschBME680 type with the physical sensor."""
        self._sensor = sensor

    def get_sensor_name(self):
        return self.SENSOR_NAME

    def get_sensor_value(self):
        raise NotImplementedError("The value read for this sensor must be implemented.")

    def get_sensor_measure(self):
        """Return the measurement unit for the sensor."""
        raise NotImplementedError("The measurement unit must be implemented by the child sensor.")


class HumidityBoschBME680(BoschBME680Type, Humidity):
    """Class which implements the humidity collected from BoschBME680 sensor module."""

    MEASURE = '% RH'

    def __init__(self, sensor):
        BoschBME680Type.__init__(self, sensor)
        Humidity.__init__(self)

    def get_sensor_value(self) -> int:
        return self._sensor.humidity

    def get_sensor_measure(self) -> str:
        return HumidityBoschBME680.MEASURE


class PressureBoschBME680(BoschBME680Type, Pressure):
    """Class which implements the pressure paired with AdafruitBME680."""

    MEASURE = 'Celsius'

    def __init__(self, sensor):
        BoschBME680Type.__init__(self, sensor)
        Pressure.__init__(self)

    def get_sensor_value(self) -> float:
        return self._sensor.pressure

    def get_sensor_measure(self) -> str:
        return PressureBoschBME680.MEASURE


class AltitudeBoschBME680(BoschBME680Type, Altitude):
    """Class which implements the altitude collected from BoschBME680 sensor module."""

    MEASURE = 'Meters'

    def __init__(self, sensor):
        BoschBME680Type.__init__(self, sensor)
        Altitude.__init__(self)

    def get_sensor_value(self) -> int:
        return self._sensor.altitude

    def get_sensor_measure(self) -> str:
        return AltitudeBoschBME680.MEASURE


class TemperatureBoschBME680(BoschBME680Type, Temperature):
    """Class which implements the temperature paired with AdafruitBME680."""

    MEASURE = 'Celsius'

    def __init__(self, sensor):
        BoschBME680Type.__init__(self, sensor)
        Temperature.__init__(self)

    def get_sensor_value(self) -> float:
        return self._sensor.temperature

    def get_sensor_measure(self) -> str:
        return TemperatureBoschBME680.MEASURE


class GasBoschBME680(BoschBME680Type, Gas):
    """Class which implements the temperature paired with AdafruitBME680."""

    MEASURE = 'gas resistance in ohms'

    def __init__(self, sensor):
        BoschBME680Type.__init__(self, sensor)
        Gas.__init__(self)

    def get_sensor_value(self) -> float:
        return self._sensor.gas

    def get_sensor_measure(self) -> str:
        return GasBoschBME680.MEASURE
