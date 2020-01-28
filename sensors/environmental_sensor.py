import time
import sys
import board
import busio
import adafruit_bme280
import adafruit_bme680

from sensors.Sensor import Sensor

sys.path.append("..")


class EnvironmentalSensor:
    I2C = busio.I2C(board.SCL, board.SDA)
    ADDRESSES = [0x77, 0x76]

    def __init__(self):
        self.sensors = []

        self.probe_sensors()

    def probe_sensors(self):
        """
        Method which probes the addresses for finding the correct bme280 sensor.
        :return: The sensor, None if not found at the provided adresses.
        """
        for address in self.ADDRESSES:
            try:
                found_sensor = adafruit_bme280.Adafruit_BME280_I2C(self.I2C, address)
                new_sensor = Sensor(found_sensor, "bme280")
                self.sensors.append(new_sensor)
                print("Sensor found at 0x%x" % address)
            except ValueError as ve:
                print(ve)
            except RuntimeError as re:
                print("These are not the sensors you're looking for.\n" + str(re))

            try:
                sensor = adafruit_bme680.Adafruit_BME680_I2C(self.I2C, address)
                self.sensors.append(Sensor(sensor, "bme680"))
                print("Sensor found at 0x%x" % address)
            except ValueError as ve:
                print(ve)
            except RuntimeError as re:
                print("These are not the sensors you're looking for.\n" + str(re))

