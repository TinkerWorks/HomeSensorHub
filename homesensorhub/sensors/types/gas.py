"""Module which contains the gas type class."""
from routing.payload import Payload
import datetime


class Gas():
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
                          self.MEASURE)
        return payload
