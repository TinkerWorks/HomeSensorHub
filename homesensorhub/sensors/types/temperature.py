"""Module which contains the temperature type class."""
from routing.payload import Payload
from sensors.types.sensor_type import SensorType

import datetime


class Temperature(SensorType):
    """Class which represents a type of value collected by a sensor."""

    TYPE = 'Temperature'

    def get_payload(self) -> Payload:
        """
        Collect payload for this sensor type.

        Trigger a data collection for this type.
        """
        payload = Payload(self.TYPE,
                          self.get_sensor_name(),
                          self.get_sensor_value(),
                          datetime.datetime.now(),
                          self.get_sensor_measure())
        return payload
