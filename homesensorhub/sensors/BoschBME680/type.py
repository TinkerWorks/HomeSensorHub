from sensors.sensor_types import Humidity, Pressure, Altitude, Temperature, Gas
from filelock import FileLock


class BoschBME680Type:

    SENSOR_NAME = 'BoschBME680'

    def __init__(self, sensor, send_payload_callback):
        """Initialise the BoschBME680 type with the physical sensor."""
        self._sensor = sensor
        self._lock = FileLock("/var/tmp/hsh_" + self.SENSOR_NAME + ".lock")

    def get_sensor_name(self):
        return self.SENSOR_NAME

    def get_sensor_value(self):
        raise NotImplementedError("The value read for this sensor must be implemented.")

    def get_sensor_measure(self):
        """Return the measurement unit for the sensor."""
        raise NotImplementedError("The measurement unit must be implemented by the child sensor.")


class HumidityBoschBME680(BoschBME680Type, Humidity):
    MEASURE = '% RH'

    def __init__(self, sensor, send_payload_callback):
        BoschBME680Type.__init__(self, sensor)
        Humidity.__init__(self, send_payload_callback)

    def get_sensor_value(self) -> int:
        with self._lock:
            return self._sensor.humidity

    def get_sensor_measure(self) -> str:
        return HumidityBoschBME680.MEASURE


class PressureBoschBME680(BoschBME680Type, Pressure):
    MEASURE = 'Celsius'

    def __init__(self, sensor, send_payload_callback):
        BoschBME680Type.__init__(self, sensor)
        Pressure.__init__(self, send_payload_callback)

    def get_sensor_value(self) -> float:
        with self._lock:
            return self._sensor.pressure

    def get_sensor_measure(self) -> str:
        return PressureBoschBME680.MEASURE


class AltitudeBoschBME680(BoschBME680Type, Altitude):
    MEASURE = 'Meters'

    def __init__(self, sensor, send_payload_callback):
        BoschBME680Type.__init__(self, sensor)
        Altitude.__init__(self, send_payload_callback)

    def get_sensor_value(self) -> int:
        with self._lock:
            return self._sensor.altitude

    def get_sensor_measure(self) -> str:
        return AltitudeBoschBME680.MEASURE


class TemperatureBoschBME680(BoschBME680Type, Temperature):
    MEASURE = 'Celsius'

    def __init__(self, sensor, send_payload_callback):
        BoschBME680Type.__init__(self, sensor)
        Temperature.__init__(self, send_payload_callback)

    def get_sensor_value(self) -> float:
        with self._lock:
            return self._sensor.temperature

    def get_sensor_measure(self) -> str:
        return TemperatureBoschBME680.MEASURE


class GasBoschBME680(BoschBME680Type, Gas):
    MEASURE = 'gas resistance in ohms'

    def __init__(self, sensor, send_payload_callback):
        BoschBME680Type.__init__(self, sensor)
        Gas.__init__(self, send_payload_callback)

    def get_sensor_value(self) -> float:
        with self._lock:
            return self._sensor.gas

    def get_sensor_measure(self) -> str:
        return GasBoschBME680.MEASURE
