"""Module which implements the sensor type interface."""
from homesensorhub.routing.payload import Payload
import datetime
from threading import Thread, Event, Timer

from homesensorhub.utils import logging
logger = logging.getLogger(__name__)


class TimedOutExc(Exception):
    pass


def deadline(timeout, *args):
    def decorate(f):
        def handler():
            logger.critical("Function deadline {}s: {}".format(timeout, f))
            raise TimedOutExc()

        def new_f(*args):
            alarm_timer = Timer(timeout, handler)
            alarm_timer.start()
            rv = f(*args)
            alarm_timer.cancel()
            return rv

        new_f.__name__ = f.__name__
        return new_f
    return decorate


class SensorType:
    """Interface for creating a sensor type object."""

    def get_properties(self) -> dict:
        return NotImplementedError("Proprieties function must be implemented by the child class.")

    def get_type(self) -> str:
        return self.TYPE

    def get_payload(self) -> Payload:
        """Collect payload for sensor measurement."""
        payload = Payload(self.TYPE,
                          self.get_sensor_name(),
                          self.get_sensor_value(),
                          datetime.datetime.now(),
                          self.get_sensor_measure())
        return payload


class SensorTypePolled(Thread, SensorType):
    """Type of sensor which is polled."""

    def __init__(self, pollrate=3, send_payload_callback=None, lock=None):
        Thread.__init__(self)
        SensorType.__init__(self)

        self.__pollrate = pollrate
        self.send_payload_callback = send_payload_callback

        self._lock = lock
        self.__stopped = Event()
        self.start()

    def run(self):
        while not self.__stopped.wait(self.__pollrate):
            if self._lock:
                self._lock.acquire()
            try:
                payload = self.get_payload()
            finally:
                if self._lock:
                    self._lock.release()

            if self.send_payload_callback:
                self.send_payload_callback(payload)
        logger.success("{} thread stopped.".format(self.get_type()))

    def stop(self):
        logger.notice("{} thread stopping.".format(self.get_type()))
        self.__stopped.set()

    def get_properties(self):
        return {
            'pollrate': CallbackPair(self.set_pollrate,
                                     self.get_pollrate)
        }

    def set_pollrate(self, pollrate):
        pollrate = pollrate.decode('utf-8')
        try:
            pollrate = float(pollrate)
            self.__pollrate = pollrate
            logger.info("Set the pollrate to the {} sensor to {}".format(self.TYPE, self.__pollrate))
        except ValueError:
            logger.info("Cannot convert pollrate to integer. The value is not an integer.")
            return

    def get_pollrate(self):
        return self.__pollrate


class SensorTypeAsynchronous(SensorType):
    """Type of sensor which is asynchronous."""

    def __init__(self):
        SensorType.__init__(self)

    def stop(self):
        pass

    def get_properties(self):
        return {}


class SensorTypeAsyncAndPolled(SensorTypeAsynchronous, SensorTypePolled):
    def __init__(self, pollrate=1, send_payload_callback=None):
        SensorTypeAsynchronous.__init__(self)
        SensorTypePolled.__init__(self, pollrate, send_payload_callback)

    def stop(self):
        SensorTypeAsynchronous.stop(self)
        SensorTypePolled.stop(self)

    def get_properties(self):
        prop = {}
        prop.update(SensorTypeAsynchronous.get_properties(self))
        prop.update(SensorTypePolled.get_properties(self))
        return prop


class Gas(SensorTypePolled):
    TYPE = 'gas'

    def __init__(self, send_payload_callback, lock):
        super().__init__(send_payload_callback=send_payload_callback, lock=lock)


class Humidity(SensorTypePolled):
    TYPE = 'humidity'

    def __init__(self, send_payload_callback, lock):
        super().__init__(send_payload_callback=send_payload_callback, lock=lock)


class Light(SensorTypePolled):
    TYPE = 'light'

    def __init__(self, send_payload_callback, lock):
        super().__init__(send_payload_callback=send_payload_callback, lock=lock)


class Pressure(SensorTypePolled):
    TYPE = 'pressure'

    def __init__(self, send_payload_callback, lock):
        super().__init__(send_payload_callback=send_payload_callback, lock=lock)


class Altitude(SensorTypePolled):
    TYPE = 'altitude'

    def __init__(self, send_payload_callback, lock):
        super().__init__(send_payload_callback=send_payload_callback, lock=lock)


class Temperature(SensorTypePolled):
    TYPE = 'temperature'

    def __init__(self, send_payload_callback, lock):
        super().__init__(send_payload_callback=send_payload_callback, lock=lock)


class Motion(SensorTypeAsyncAndPolled):
    TYPE = 'motion'

    def __init__(self, pollrate, send_payload_callback):
        SensorTypeAsyncAndPolled.__init__(self, pollrate=pollrate, send_payload_callback=send_payload_callback)


class CallbackPair:
    """Create a setter getter object type for access to sensor properties."""

    def __init__(self, setter, getter):
        self.setter = setter
        self.getter = getter
