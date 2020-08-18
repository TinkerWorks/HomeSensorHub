"""Module which contains the gas type class."""
from routing.payload import Payload
from sensors.types.sensor_type import SensorType

import datetime


class Gas(SensorType):
    """Class which represents a type of value collected by a sensor."""

    TYPE = 'Gas'

    def get_payload(self) -> Payload:
        """
        Collect payload for the gas.

        Triggers a data read on the sensor for this type.
        """
        payload = Payload(self.TYPE,
                          self.get_sensor_name(),
                          self.get_sensor_value(),
                          datetime.datetime.now(),
                          self.get_sensor_measure())
        return payload
