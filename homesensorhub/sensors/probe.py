"""Module which implements the interface for sensor probing."""
from filelock import FileLock
import os


class Probe:
    """Class which implements the interface for sensor probing."""

    @classmethod
    def probe(cls, send_payload_callback=None) -> list:

        lock_file = "/tmp/hsh_" + cls.get_sensor_name() + ".lock"
        lock = FileLock(lock_file)

        with lock:
            try:
                os.chmod(lock_file, 0o777)
            except PermissionError:
                pass

            return cls.functional_probe(cls, send_payload_callback, lock)
