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
                self.sensor = adafruit_bme280.Adafruit_BME280_I2C(self.I2C, address)
                print("Sensor found at 0x%x" % address)
                print(type(self.sensor))
            except ValueError as ve:
                print(ve)
            except RuntimeError as re:
                print("These are not the sensors you're looking for.\n" + str(re))

            try:
                self.sensor = adafruit_bme680.Adafruit_BME680_I2C(self.I2C, address)
                print("Sensor found at 0x%x" % address)
                print(type(self.sensor))
            except ValueError as ve:
                print(ve)
            except RuntimeError as re:
                print("These are not the sensors you're looking for.\n" + str(re))

    def collect_data(self) -> dict:
        """
        Collect environmental data from the sensor and update self.data_packet
        :return: None
        """
        data_packet = {}

        if self.sensor is not None:
            data_packet['temperature'] = self.sensor.temperature
            data_packet['humidity'] = self.sensor.humidity
            data_packet['pressure'] = self.sensor.pressure
            data_packet['altitude'] = self.sensor.altitude

            try:
                data_packet['gas'] = self.sensor.gas
            except AttributeError:
                pass

        else:
            print("Sensor not correctly set.")

        return data_packet


if __name__ == "__main__":
    test = EnvironmentalSensor()

    while True:
        data = test.collect_data()
        print(data)
        time.sleep(2)
