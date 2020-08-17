"""Module which contains the light type class."""
from routing.payload import Payload
import datetime


class Light():
    """Class which represents a type of light value collected by light sensor modules."""

    TYPE = 'Light'

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
