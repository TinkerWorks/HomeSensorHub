"""Module which implements the sensor type interface."""
from routing.payload import Payload
import datetime


class SensorType:
    """Interface for creating a sensor type object."""

    def get_payload(self) -> Payload:
        """Collect payload for sensor measurement."""
        payload = Payload(self.TYPE,
                          self.get_sensor_name(),
                          self.get_sensor_value(),
                          datetime.datetime.now(),
                          self.get_sensor_measure())
        return payload


class Gas(SensorType):
    TYPE = 'Gas'


class Humidity(SensorType):
    TYPE = 'Humidity'


class Light(SensorType):
    TYPE = 'Light'


class Pressure(SensorType):
    TYPE = 'Pressure'


class Altitude(SensorType):
    TYPE = 'Altitude'


class Temperature(SensorType):
    TYPE = 'Temperature'

    
class Motion(SensorType):
    TYPE = 'Motion'
