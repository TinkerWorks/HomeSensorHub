import time

from sensors.environmental_sensor import EnvironmentalSensor


class SensorMonitor:
    """
    Class which will hold the information of all the types of sensors and their data. This will represent the data
    communicator.
    """

    ENVIRONMENTAL_SENSORS = None

    def __init__(self):
        self.data = {}
        self.ENVIRONMENTAL_SENSORS = EnvironmentalSensor()

    def collect_data(self, sensor_type) -> None:
        """
        Since all of the types (eg. environmental, motion, light) can have multiple sensors, over a call we get the data
        from all the type's sensors, for now.
        """
        for sensor in sensor_type.sensors:
            data = sensor.get_data()
            self.data.update(data)


if __name__ == "__main__":
    se = SensorMonitor()

    while True:
        se.collect_data(se.ENVIRONMENTAL_SENSORS)
        print(se.data)

        time.sleep(1)
