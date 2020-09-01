"""Module which implements the sensor type interface."""
from routing.payload import Payload
import datetime
from threading import Thread, Event


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

    def __init__(self, pollrate=3, send_payload_callback=None):
        Thread.__init__(self)
        SensorType.__init__(self)

        self.__pollrate = pollrate
        self.send_payload_callback = send_payload_callback

        self.__stopped = Event()
        self.start()

    def run(self):
        while not self.__stopped.wait(self.__pollrate):
            payload = self.get_payload()
            if self.send_payload_callback:
                self.send_payload_callback(payload)

    def stop(self):
        print("{} thread stopped.".format(self.get_type()))
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
            print("Set the pollrate to the {} sensor to {}".format(self.TYPE, self.__pollrate))
        except ValueError:
            print("Cannot convert pollrate to integer. The value is not an integer.")
            return

    def get_pollrate(self):
        return self.__pollrate


class SensorTypeAsynchronous(SensorType):
    """Type of sensor which is asynchronous."""

    def __init__(self):
        pass

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

    def __init__(self, send_payload_callback):
        super().__init__(send_payload_callback=send_payload_callback)


class Humidity(SensorTypePolled):
    TYPE = 'humidity'

    def __init__(self, send_payload_callback):
        super().__init__(send_payload_callback=send_payload_callback)


class Light(SensorTypePolled):
    TYPE = 'light'

    def __init__(self, send_payload_callback):
        super().__init__(send_payload_callback=send_payload_callback)


class Pressure(SensorTypePolled):
    TYPE = 'pressure'

    def __init__(self, send_payload_callback):
        super().__init__(send_payload_callback=send_payload_callback)


class Altitude(SensorTypePolled):
    TYPE = 'altitude'

    def __init__(self, send_payload_callback):
        super().__init__(send_payload_callback=send_payload_callback)


class Temperature(SensorTypePolled):
    TYPE = 'temperature'

    def __init__(self, send_payload_callback):
        super().__init__(send_payload_callback=send_payload_callback)


class Motion(SensorTypeAsyncAndPolled):
    TYPE = 'motion'

    def __init__(self, pollrate, send_payload_callback):
        SensorTypeAsyncAndPolled.__init__(self, pollrate=pollrate, send_payload_callback=send_payload_callback)


class CallbackPair:
    """Create a setter getter object type for access to sensor properties."""

    def __init__(self, setter, getter):
        self.setter = setter
        self.getter = getter
