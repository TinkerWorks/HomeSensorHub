"""Module which contains the pressure type class."""
from routing.payload import Payload
import datetime


class Pressure():
    """Class which represents a type of value collected by a sensor."""

    TYPE = 'Pressure'

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
