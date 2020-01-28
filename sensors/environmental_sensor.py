import board
import busio
import adafruit_bme280
import adafruit_bme680

from sensors.sensor import Sensor


class EnvironmentalSensor:
    I2C = busio.I2C(board.SCL, board.SDA)
    ADDRESSES = [0x77, 0x76]

    def __init__(self):
        self.sensors = []

        self.probe_sensors()

    def probe_sensors(self):
        """
        Method which probes each address in order to find the location of the mounted sensor device.
        :return: The sensor, None if not found at the provided addresses.
        """
        for address in self.ADDRESSES:
            try:
                found_sensor = adafruit_bme280.Adafruit_BME280_I2C(self.I2C, address)
                self.sensors.append(Sensor(found_sensor, "bme280"))
                print("Sensor found at 0x%x" % address)
            except ValueError as ve:
                print(ve)
            except RuntimeError as re:
                print("These are not the sensors you're looking for.\n" + str(re))

            try:
                found_sensor = adafruit_bme680.Adafruit_BME680_I2C(self.I2C, address)
                self.sensors.append(Sensor(found_sensor, "bme680"))
                print("Sensor found at 0x%x" % address)
            except ValueError as ve:
                print(ve)
            except RuntimeError as re:
                print("These are not the sensors you're looking for.\n" + str(re))

