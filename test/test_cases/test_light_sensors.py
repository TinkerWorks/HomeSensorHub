
import sys
print(str(sys.path))

from sensors.light_sensor import LightSensor
import unittest
import time



class TestLightSensors(unittest.TestCase):

    def test_light_sensor_sent_value(self):
        time_end = time.time() + 60
        collecetd_data = []

        while time.time() < time_end:
            light_sensor = LightSensor("test_light")

            collecetd_data.append(light_sensor.get_data(interval=1))

            time.sleep(1)

        if len(collecetd_data) == 0:
            raise Exception("No value gathered from light sensor.")
