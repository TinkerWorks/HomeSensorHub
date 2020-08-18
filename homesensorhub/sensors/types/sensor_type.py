"""Module which implements the sensor type interface."""
from routing.payload import Payload


class SensorType:
    """Interface for creating a sensor type object."""
    
    def get_payload(self) -> Payload:
        raise NotImplementedError("Get payload function must be implemented in each child class.")
