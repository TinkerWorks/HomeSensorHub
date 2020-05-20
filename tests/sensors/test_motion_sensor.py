import sys

#TODO: This is a way, but overriding __import__ might be better
from mock import Mock,MagicMock
if 'RPi' not in sys.modules.keys():
    sys.modules['RPi'] = Mock()
if 'RPi.GPIO' not in sys.modules.keys():
    sys.modules['RPi.GPIO'] = Mock()

from sensors.motion_sensor import MotionSensor

import unittest

class MotionSensorTests(unittest.TestCase):
    def test_Init(self):
        ms = MotionSensor()
        ms.initialize()
