
import sys

from mock import Mock
if 'sensors.drivers.TSL258x' not in sys.modules.keys():
    sys.modules['sensors.drivers.TSL258x'] = Mock()
if 'sensors.drivers' not in sys.modules.keys():
    sys.modules['sensors.drivers'] = Mock()

from sensors.drivers.TSL258x import TSL258x
from sensors.types.TSL258x.light_TSL258x import LightTSL258x
from sensors.probes.probe_TSL258x import ProbeTSL258x

import unittest
import time
import random


class TestLightSensors(unittest.TestCase):

    def test_light_sensor_sent_value(self):

        ls = TSL258x()
        TSL258x.probe.return_value = ls

        time_end = time.time() + 1

        while time.time() < time_end:
            # ls_probe = LightSensorProbe()
            sensors = ProbeTSL258x().probe()

            for sensor in sensors:
                ls.read.return_value = random.randint(0, 200.000)
                actual_data = str(sensor.get_sensor_value())
                self.assertEquals(actual_data, str(ls.read.return_value))

            time.sleep(0.1)

        if len(actual_data) == 0:
            raise Exception("No value gathered from light sensor.")
