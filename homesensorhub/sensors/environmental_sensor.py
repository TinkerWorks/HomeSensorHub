import logging
import time

import board
import busio
import adafruit_bme280
import adafruit_bme680


logging.basicConfig(level=logging.INFO)


class EnvironmentalSensor:
    def __init__(self, sensor, name):
        self.sensor = sensor
        self.name = name
        self.data_packet = None

    def set_sea_level_pressure(self, sea_level_pressure) -> None:
        """
        Used for altitude determination.
        """
        self.sensor.sea_level_pressure = sea_level_pressure

    def get_sensor_name(self) -> str:
        """
        Function which returns the actual name of the sensor (eg. BME280, BME680 etc.).
        """
        return self.name

    def get_data(self) -> dict:
        self.collect_data()
        return self.data_packet

    def collect_data(self) -> None:
        self.data_packet = {'temperature': self.sensor.temperature,
                            'humidity': self.sensor.humidity,
                            'pressure': self.sensor.pressure,
                            'altitude': self.sensor.altitude
                            }

        try:
            self.data_packet['gas'] = self.sensor.gas
        except AttributeError:
            pass


class EnvironmentalSensorProbe:
    I2C = busio.I2C(board.SCL, board.SDA)
    ADDRESSES = [0x77, 0x76]

    def __init__(self):
        self.sensors = []

        self.probe_sensors()

    def probe_sensors(self) -> None:
        """
        Function which iterates over multiple I2C addresses and sensors probing in the case we have multiple
        types on the same device (eg. BME280, BME680, etc.). In case multiple sensors are connected to the same
        device, we need to correctly assign the sensor to its I2C address.
        :return: None
        """
        sensor_choices = {
            (adafruit_bme280.Adafruit_BME280_I2C, "bme280"),
            (adafruit_bme680.Adafruit_BME680_I2C, "bme680")
        }

        for address in self.ADDRESSES:
            for sensor in sensor_choices:
                sensor_probe_function = sensor[0]
                sensor_pretty_name = sensor[0]
                try:
                    found_sensor = sensor_probe_function(self.I2C, address)
                    self.sensors.append(EnvironmentalSensor(found_sensor, sensor_pretty_name))
                    logging.info("Environmental Sensor {} found at {}".format(sensor_pretty_name, hex(address)))
                except ValueError as ve:
                    logging.debug(ve)
                except RuntimeError as re:
                    logging.info("These are not the sensors you're looking for.\n")
                    logging.debug(re)

        print(str(self.sensors))

if __name__ == "__main__":
    test = EnvironmentalSensorProbe()

    while True:
        for sensor in test.sensors:
            data = sensor.get_data()
            logging.info(data)
            time.sleep(2)
