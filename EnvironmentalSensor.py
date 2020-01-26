import time

import board
import busio
import adafruit_bme280
import adafruit_bme680


class EnvironmentalSensor:
    I2C = busio.I2C(board.SCL, board.SDA)
    ADDRESSES = [0x77, 0x76]
    SEA_LEVEL_PRESSURE = 1013.25

    def __init__(self):
        self.sensor = None
        self.probe_sensor()
        self.data_packet = {}

        if self.sensor is not None:
            self.sensor.sea_level_pressure = self.SEA_LEVEL_PRESSURE

    def probe_sensor(self):
        """
        Method which probes the addresses for finding the correct bme280 sensor.
        :return: The sensor, None if not found at the provided adresses.
        """
        for address in self.ADDRESSES:
            try:
                self.sensor = adafruit_bme280.Adafruit_BME280_I2C(self.I2C, self.ADDRESSES)
                print("Sensor found at 0x%x" % address)
                print(type(self.sensor))
            except ValueError as ve:
                print(ve)

            try:
                self.sensor = adafruit_bme680.Adafruit_BME680_I2C(self.I2C, self.ADDRESSES)
                print("Sensor found at 0x%x" % address)
                print(type(self.sensor))
            except ValueError as ve:
                print(ve)

    def collect_data(self) -> None:
        """
        Collect environmental data from the sensor and update self.data_packet
        :return: None
        """
        self.data_packet['TEMPERATURE'] = self.sensor.temperature
        self.data_packet['HUMIDITY'] = self.sensor.humidity
        self.data_packet['PRESSURE'] = self.sensor.pressure
        self.data_packet['ALTITUDE'] = self.sensor.altitude

        try:
            self.data_packet['GAS'] = self.sensor.gas
        except AttributeError:
            self.data_packet['GAS'] = None


if __name__ == "__main__":
    pass