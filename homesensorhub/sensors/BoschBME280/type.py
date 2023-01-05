from homesensorhub.sensors.sensor_types import Humidity, Pressure, Altitude, Temperature, deadline
from threading import Lock

from homesensorhub.utils import logging
logger = logging.getLogger(__name__)

lock = Lock()


class BoschBME280Type:

    SENSOR_NAME = 'BoschBME280'

    def __init__(self, sensor):
        """Initialise the BoschBME280 type with the physical sensor."""
        self._sensor = sensor

    def get_sensor_name(self):
        return self.SENSOR_NAME

    def get_sensor_value(self):
        raise NotImplementedError("The value read for this sensor must be implemented.")

    def get_sensor_measure(self):
        """Return the measurement unit for the sensor."""
        raise NotImplementedError("The measurement unit must be implemented by the child sensor.")


class HumidityBoschBME280(BoschBME280Type, Humidity):
    MEASURE = '% RH'

    def __init__(self, sensor, send_payload_callback, lock):
        BoschBME280Type.__init__(self, sensor)
        Humidity.__init__(self, send_payload_callback, lock)

    @deadline(5)
    def get_sensor_value(self) -> int:
        with lock:
            logger.spam("Getting sensor humidity value")
            h = self._sensor.humidity
            logger.spam("Get sensor humidity value done")
        return h

    def get_sensor_measure(self) -> str:
        return HumidityBoschBME280.MEASURE


class PressureBoschBME280(BoschBME280Type, Pressure):
    MEASURE = 'Celsius'

    def __init__(self, sensor, send_payload_callback, lock):
        BoschBME280Type.__init__(self, sensor)
        Pressure.__init__(self, send_payload_callback, lock)

    @deadline(5)
    def get_sensor_value(self) -> float:
        with lock:
            logger.spam("Getting sensor pressure value")
            p = self._sensor.pressure
            logger.spam("Get sensor pressure value done")
        return p

    def get_sensor_measure(self) -> str:
        return PressureBoschBME280.MEASURE


class AltitudeBoschBME280(BoschBME280Type, Altitude):
    MEASURE = 'Meters'

    def __init__(self, sensor, send_payload_callback, lock):
        BoschBME280Type.__init__(self, sensor)
        Altitude.__init__(self, send_payload_callback, lock)

    @deadline(5)
    def get_sensor_value(self) -> int:
        with lock:
            logger.spam("Getting sensor altitude value")
            a = self._sensor.altitude
            logger.spam("Get sensor altitude value done")
        return a

    def get_sensor_measure(self) -> str:
        return AltitudeBoschBME280.MEASURE


class TemperatureBoschBME280(BoschBME280Type, Temperature):
    MEASURE = 'Celsius'

    def __init__(self, sensor, send_payload_callback, lock):
        BoschBME280Type.__init__(self, sensor)
        Temperature.__init__(self, send_payload_callback, lock)

    @deadline(5)
    def get_sensor_value(self) -> float:
        with lock:
            logger.spam("Getting sensor temperature value")
            t = self._sensor.temperature
            logger.spam("Get sensor temperature value done")
        return t

    def get_sensor_measure(self) -> str:
        return TemperatureBoschBME280.MEASURE
