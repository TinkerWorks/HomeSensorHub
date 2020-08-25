
import sys

from mock import Mock
if 'sensors.TSL258x.driver' not in sys.modules.keys():
    sys.modules['sensors.TSL258x.driver'] = Mock()


from sensors.TSL258x.driver import TSL258x
from sensors.TSL258x.type import LightTSL258x
from sensors.TSL258x.probe import ProbeTSL258x

import unittest
import time
import random


class TestLightSensors(unittest.TestCase):

    def test_light_sensor_sent_value(self):

        ls = TSL258x()
        TSL258x.probe.return_value = ls

        time_end = time.time() + 1

        sensors = ProbeTSL258x().probe()

        while time.time() < time_end:
            for sensor in sensors:
                ls.read.return_value = random.randint(0, 200.000)
                actual_data = str(sensor.get_sensor_value())
                self.assertEquals(actual_data, str(ls.read.return_value))

            time.sleep(0.1)

        if len(actual_data) == 0:
            raise Exception("No value gathered from light sensor.")

        for sensor in sensors:
            sensor.stop()
