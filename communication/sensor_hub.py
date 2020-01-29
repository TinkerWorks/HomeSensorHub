import time

from sensors.environmental_sensor import EnvironmentalSensor


class SensorHub:
    """
    Class which will hold the information of all the types of sensors and their data. This will represent the data
    communicator.
    """

    def __init__(self):
        self.data = {}

        self.environmental_sensors = EnvironmentalSensor()

        self.all_sensors = [self.environmental_sensors]
        # TODO use getattr to iterate only over the sensors instead of hardcoding them into a list.

    def collect_data_from(self, sensor_type) -> None:
        """
        Since all of the types (eg. environmental, motion, light) can have multiple sensors, over a call we get the data
        from all the type's sensors, for now.
        """
        for sensor in sensor_type.sensors:
            data = sensor.get_data()
            print(data)
            self.data.update(data)

    def collect_all_data(self):
        for sensor in self.all_sensors:
            self.collect_data_from(sensor)


if __name__ == "__main__":
    se = SensorHub()

    while True:
        # se.collect_data_from(se.environmental_sensors)
        se.collect_all_data()
        # print(se.data)

        time.sleep(1)
