"""Module which contains the altitude type class."""
from routing.payload import Payload
from sensors.types.sensor_type import SensorType

import datetime


class Altitude(SensorType):
    """Class which represents a type of value collected by a sensor."""

    TYPE = 'Altitude'

    def get_payload(self) -> Payload:
        """
        Collect payload for the altitude.

        Triggers a data read on the sensor for this type.
        """
        payload = Payload(self.TYPE,
                          self.get_sensor_name(),
                          self.get_sensor_value(),
                          datetime.datetime.now(),
                          self.get_sensor_measure())
        return payload
