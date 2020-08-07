
"""Module which implements the classes for sending collected data to MQTT."""


class DataSender:
    """Class which acts as a virtual class for a sink."""

    def __init__(self):
        """Will be overwritten by child."""
        pass

    def connect(self, retry):
        """Set up connection with a sink."""
        pass

    def send(self, data):
        """Send the collected data to a sink."""
        pass
