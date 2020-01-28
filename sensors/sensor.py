

class Sensor:
    def __init__(self, sensor, name):
        self.sensor = sensor
        self.name = name
        self.data_packet = None

    def set_sea_level_pressure(self, sea_level_pressure):
        self.sensor.sea_level_pressure = sea_level_pressure

    def get_sensor_name(self):
        return self.name

    def get_data(self):
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
