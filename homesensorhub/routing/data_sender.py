
"""Module which implements the classes for sending collected data to MQTT."""


class DataSender:
    """Class which acts as a virtual class for a sink."""

    def connect(self, retry):
        """Set up connection with a sink."""
        raise NotImplementedError("The child sender must implement the connect function.")

    def send(self, data):
        """Send the collected data to a sink."""
        raise NotImplementedError("The child sender must implement the send function.")
