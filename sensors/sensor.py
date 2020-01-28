class Sensor:
    def __init__(self, sensor, name):
        self.sensor = sensor
        self.name = name
        self.data_packet = None

    def set_sea_level_pressure(self, sea_level_pressure) -> None:
        """
        Function which sets the sea level pressure for calculating the altitude.
        :param sea_level_pressure: Pressure at sea level.
        :return: None
        """
        self.sensor.sea_level_pressure = sea_level_pressure

    def get_sensor_name(self) -> str:
        """
        Function which returns the name of the sensor. Ex: bme280, bme680...
        :return:
        """
        return self.name

    def get_data(self) -> dict:
        """
        Function which returns the data collected from the sensor at the moment of calling.
        :return: Information from the sensors (temperature, humidity...) in the form of a dictionary with
        key: value's name; value: value.
        """
        self.collect_data()
        return self.data_packet

    def collect_data(self) -> None:
        """
        Collect environmental data from the sensor.
        :return: None
        """

        self.data_packet = {'temperature': self.sensor.temperature,
                            'humidity': self.sensor.humidity,
                            'pressure': self.sensor.pressure,
                            'altitude': self.sensor.altitude
                            }

        try:
            self.data_packet['gas'] = self.sensor.gas
        except AttributeError:
            pass
