"""Module which implements the payload class."""
import json


class Payload:
    """Class which implements the configuration of the payload for MQTT."""

    def __init__(self, type, name, value, timestamp, measurement):
        """Structure the data received from the sensors."""
        self.__type = type
        self.__name = name
        self.__value = value
        self.__timestamp = timestamp
        self.__measurement = measurement

    def get_string_payload(self) -> dict:
        """Return the payload of collected data for a sensor type."""
        payload = {'type': self.get_str_type(),
                   'name': self.get_str_name(),
                   'value': self.get_str_value(),
                   'timestamp': self.get_str_timestamp(),
                   'measurement': self.get_str_measurement()}
        return payload

    def get_json_payload(self) -> json.dumps:
        """
        Construct the json payload based on the collected data.

        The accepted values for MQTT payload are None, Int, Float and str, so
        before trying to send the raw data from the sensors through MQTT, it
        needs to be refined into an accepted form.
        """
        json_payload = json.dumps(self.get_string_payload(),
                                  indent=4)
        return json_payload

    def get_str_type(self) -> str:
        """
        Return the type of the sensor in string format.

        Needed for topic creation in MQTT.
        """
        return str(self.__type)

    def get_str_name(self) -> str:
        """Return the name of the sensor in string format."""
        return str(self.__name)

    def get_str_value(self) -> str:
        """Return the value collected by the sensor in string format."""
        return "{}".format(round(self.__value, 2))

    def get_str_timestamp(self) -> str:
        """Return the timestamp of the value extraction in string format."""
        return str(self.__timestamp)

    def get_str_measurement(self) -> str:
        """Return the unit of measurement for the value in string format."""
        return str(self.__measurement)
