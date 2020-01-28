import time

from sensors.environmental_sensor import EnvironmentalSensor
from sensors.sensor import Sensor

if __name__ == "__main__":
    environmental = EnvironmentalSensor()

    while True:
        for sensor in environmental.sensors:
            data = sensor.get_data()
            print(data)
            time.sleep(2)
