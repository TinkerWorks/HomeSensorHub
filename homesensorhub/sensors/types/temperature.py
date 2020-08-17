"""Module which contains the temperature type class."""
from routing.payload import Payload
import datetime

class Temperature():
    """Class which represents a type of value collected by a sensor."""

    TYPE = 'Temperature'

    def __init__(self):
        """Set up the Temperature object."""
        pass

    def get_payload(self) -> Payload:
        """
        Collect payload for this sensor type.

        Trigger a data collection for this type.
        """
        payload = Payload(self.TYPE,
                          self.get_sensor_name(),
                          self.get_sensor_value(),
                          datetime.datetime.now(),
                          self.MEASURE)
        return payload
