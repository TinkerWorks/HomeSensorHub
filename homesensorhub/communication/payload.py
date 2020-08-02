"""Module which implements the payload class."""
import json


class Payload:
    """Class which implements the configuration of the payload for MQTT."""

    def __init__(self, packet):
        """Extract and structure the data from the packet."""
        try:
            self.__type = packet['type']
            self.__name = packet['name']
            self.__value = packet['value']
            self.__timestamp = packet['timestamp']
            self.__measurement = packet['measurement']
        except KeyError as error:
            print("The requested key is not available in the packet:\n{}"
                  .format(error))

    def get_mqtt_payload(self) -> json.dumps:
        """
        Construct the MQTT payload based on the received packet.

        The accepted values for MQTT payload are None, Int, Float and str, so
        before trying to send the raw data from the sensors through MQTT, it
        needs to be refined into a readable string form.
        """
        payload = {
            'type': self.__get_str_type(),
            'name': self.__get_str_name(),
            'value': self.__get_str_value(),
            'timestamp': self.__get_str_timestamp(),
            'measurement': self.__get_str_measurement()
        }

        json_payload = json.dumps(payload,
                                  indent=4,
                                  separators=(". ", " = "),
                                  sort_keys=True)
        return json_payload

    def __get_str_type(self):
        return str(self.__type)

    def __get_str_name(self):
        return str(self.__name)

    def __get_str_value(self):
        return "{}".format(round(self.__value, 2))

    def __get_str_timestamp(self):
        return str(self.__timestamp)

    def __get_str_measurement(self):
        return str(self.__measurement)
