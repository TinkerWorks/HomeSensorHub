import time

from sensors.environmental_sensor import EnvironmentalSensor

if __name__ == "__main__":
    environmental = EnvironmentalSensor()

    while True:
        for sensor in environmental.sensors:
            data = sensor.get_data()
            print(data)
            time.sleep(2)
