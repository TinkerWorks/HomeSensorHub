from sensors.sensor_types import Humidity, Pressure, Altitude, Temperature, Gas

from utils import logging
logger = logging.getLogger(__name__)


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
    MEASURE = '% RH'

    def __init__(self, sensor, send_payload_callback, lock):
        BoschBME680Type.__init__(self, sensor)
        Humidity.__init__(self, send_payload_callback, lock)

    def get_sensor_value(self) -> int:
        logger.spam("Getting sensor humidity value")
        h = self._sensor.humidity
        logger.spam("Get sensor humidity value done")
        return h

    def get_sensor_measure(self) -> str:
        return HumidityBoschBME680.MEASURE


class PressureBoschBME680(BoschBME680Type, Pressure):
    MEASURE = 'Celsius'

    def __init__(self, sensor, send_payload_callback, lock):
        BoschBME680Type.__init__(self, sensor)
        Pressure.__init__(self, send_payload_callback, lock)

    def get_sensor_value(self) -> float:
        logger.spam("Getting sensor pressure value")
        p = self._sensor.pressure
        logger.spam("Get sensor pressure value done")
        return p

    def get_sensor_measure(self) -> str:
        return PressureBoschBME680.MEASURE


class AltitudeBoschBME680(BoschBME680Type, Altitude):
    MEASURE = 'Meters'

    def __init__(self, sensor, send_payload_callback, lock):
        BoschBME680Type.__init__(self, sensor)
        Altitude.__init__(self, send_payload_callback, lock)

    def get_sensor_value(self) -> int:
        logger.spam("Getting sensor altitude value")
        a = self._sensor.altitude
        logger.spam("Get sensor altitude value done")
        return a

    def get_sensor_measure(self) -> str:
        return AltitudeBoschBME680.MEASURE


class TemperatureBoschBME680(BoschBME680Type, Temperature):
    MEASURE = 'Celsius'

    def __init__(self, sensor, send_payload_callback, lock):
        BoschBME680Type.__init__(self, sensor)
        Temperature.__init__(self, send_payload_callback, lock)

    def get_sensor_value(self) -> float:
        logger.spam("Getting sensor temperature value")
        t = self._sensor.temperature
        logger.spam("Get sensor temperature value done")
        return t

    def get_sensor_measure(self) -> str:
        return TemperatureBoschBME680.MEASURE


class GasBoschBME680(BoschBME680Type, Gas):
    MEASURE = 'gas resistance in ohms'

    def __init__(self, sensor, send_payload_callback, lock):
        BoschBME680Type.__init__(self, sensor)
        Gas.__init__(self, send_payload_callback, lock)

    def get_sensor_value(self) -> float:
        logger.spam("Getting sensor gas value")
        g = self._sensor.gas
        logger.spam("Get sensor gas value done")
        return g

    def get_sensor_measure(self) -> str:
        return GasBoschBME680.MEASURE
