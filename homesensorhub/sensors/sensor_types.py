"""Module which implements the sensor type interface."""
from routing.payload import Payload
import datetime


class SensorType:
    """Interface for creating a sensor type object."""

    def get_properties(self) -> dict:
        return NotImplementedError("Proprieties function must be implemented by the child class.")

    def get_payload(self) -> Payload:
        """Collect payload for sensor measurement."""
        payload = Payload(self.TYPE,
                          self.get_sensor_name(),
                          self.get_sensor_value(),
                          datetime.datetime.now(),
                          self.get_sensor_measure())
        return payload


class SensorTypePolled(SensorType):
    """Type of sensor which is polled."""

    def __init__(self, pollrate=3):
        self.pollrate = pollrate

    def get_properties(self):
        return {
            'pollrate': self.pollrate
        }


class SensorTypeAsynchronous(SensorType):
    """Type of sensor which is asynchronous."""

    def get_properties(self):
        return {}


class Gas(SensorTypePolled):
    TYPE = 'gas'


class Humidity(SensorTypePolled):
    TYPE = 'humidity'


class Light(SensorTypePolled):
    TYPE = 'light'


class Pressure(SensorTypePolled):
    TYPE = 'pressure'


class Altitude(SensorTypePolled):
    TYPE = 'altitude'


class Temperature(SensorTypePolled):
    TYPE = 'temperature'


class Motion(SensorTypeAsynchronous):
    TYPE = 'motion'
