from sensors.sensor_types import Humidity, Pressure, Altitude, Temperature
from filelock import FileLock


class BoschBME280Type:

    SENSOR_NAME = 'BoschBME280'

    def __init__(self, sensor):
        """Initialise the BoschBME280 type with the physical sensor."""
        self._sensor = sensor
        self._lock = FileLock("/var/tmp/hsh_" + self.SENSOR_NAME + ".lock")

    def get_sensor_name(self):
        return self.SENSOR_NAME

    def get_sensor_value(self):
        raise NotImplementedError("The value read for this sensor must be implemented.")

    def get_sensor_measure(self):
        """Return the measurement unit for the sensor."""
        raise NotImplementedError("The measurement unit must be implemented by the child sensor.")


class HumidityBoschBME280(BoschBME280Type, Humidity):
    MEASURE = '% RH'

    def __init__(self, sensor, send_payload_callback):
        BoschBME280Type.__init__(self, sensor)
        Humidity.__init__(self, send_payload_callback)

    def get_sensor_value(self) -> int:
        with self._lock:
            return self._sensor.humidity

    def get_sensor_measure(self) -> str:
        return HumidityBoschBME280.MEASURE


class PressureBoschBME280(BoschBME280Type, Pressure):
    MEASURE = 'Celsius'

    def __init__(self, sensor, send_payload_callback):
        BoschBME280Type.__init__(self, sensor)
        Pressure.__init__(self, send_payload_callback)

    def get_sensor_value(self) -> float:
        with self._lock:
            return self._sensor.pressure

    def get_sensor_measure(self) -> str:
        return PressureBoschBME280.MEASURE


class AltitudeBoschBME280(BoschBME280Type, Altitude):
    MEASURE = 'Meters'

    def __init__(self, sensor, send_payload_callback):
        BoschBME280Type.__init__(self, sensor)
        Altitude.__init__(self, send_payload_callback)

    def get_sensor_value(self) -> int:
        with self._lock:
            return self._sensor.altitude

    def get_sensor_measure(self) -> str:
        return AltitudeBoschBME280.MEASURE


class TemperatureBoschBME280(BoschBME280Type, Temperature):
    MEASURE = 'Celsius'

    def __init__(self, sensor, send_payload_callback):
        BoschBME280Type.__init__(self, sensor)
        Temperature.__init__(self, send_payload_callback)

    def get_sensor_value(self) -> float:
        with self._lock:
            return self._sensor.temperature

    def get_sensor_measure(self) -> str:
        return TemperatureBoschBME280.MEASURE
