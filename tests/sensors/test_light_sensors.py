
import sys

from mock import Mock
if 'sensors.drivers.TSL258x' not in sys.modules.keys():
    sys.modules['sensors.drivers.TSL258x'] = Mock()
if 'sensors.drivers' not in sys.modules.keys():
    sys.modules['sensors.drivers'] = Mock()

from sensors.drivers.TSL258x import TSL258x
from sensors.light_sensor import LightSensor, LightSensorProbe

import unittest
import time
import random


class TestLightSensors(unittest.TestCase):

    def test_light_sensor_sent_value(self):

        ls = TSL258x()
        TSL258x.probe.return_value = ls

        time_end = time.time() + 1

        while time.time() < time_end:
            ls_probe = LightSensorProbe()

            for sensor in ls_probe.get_sensors():
                ls.read.return_value = random.randint(0, 200.000)

                collected_data = sensor.get_data()
                payload = collected_data[0]
                actual_data = payload.get_value()

                self.assertEquals(actual_data, ls.read.return_value)

            time.sleep(0.1)

        if len(collected_data) == 0:
            raise Exception("No value gathered from light sensor.")
