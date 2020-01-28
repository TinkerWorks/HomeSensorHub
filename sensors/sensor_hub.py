import time

import board
import busio


class SensorMonitor:

    ENVIRONMENTAL_SENSORS = None
    MOTION_SENSORS = None

    def __init__(self):
        self.data = {}
        self.ENVIRONMENTAL_SENSORS = EnvironmentalSensors()
        # TODO self.MOTION_SENSORS = MovementSensors()\

    def collect_data(self):
        while True:
            environmental_data = self.ENVIRONMENTAL_SENSORS.collect_data()
            # TODO motion_data = self.MOTION_SENSORS.collect_data()

            self.data.update(environmental_data)
            # TODO self.data.update(motion_data)

            time.sleep(2)


