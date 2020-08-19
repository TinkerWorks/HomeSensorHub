"""Module which implements the interface for sensor probing."""


class Probe:
    """Class which implements the interface for sensor probing."""

    @classmethod
    def probe(cls, send_payload_callback=None) -> list:
        """Probe for a specific sensor on the board."""
        raise NotImplementedError("Probing must be implemented in each child probe class.")
