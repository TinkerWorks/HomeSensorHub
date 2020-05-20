import sys

#TODO: This is a way, but overriding __import__ might be better
from mock import Mock,MagicMock
if 'RPi' not in sys.modules.keys():
    sys.modules['RPi'] = Mock()
if 'RPi.GPIO' not in sys.modules.keys():
    sys.modules['RPi.GPIO'] = Mock()

import RPi.GPIO as GPIO

from sensors.motion_sensor import MotionSensor

import unittest

class MotionSensorTests(unittest.TestCase):

    PIN = 3

    def test_NormalTransitions(self):
        motionCallback = Mock()
        ms = MotionSensor(self.PIN, motionCallback)
        ms.initialize()

        #Record GPIO callback method
        GPIOcallback=GPIO.add_event_detect.mock_calls[0][2]['callback']

        state_transition = [
            (1, True),
            (0, False),
            (1, True),
            (0, False),
        ]

        # Fake it .... till you make it ...
        for transition in state_transition:
            gpio_value = transition[0]
            next_state = transition[1]

            motionCallback.reset_mock()

            GPIO.input.return_value = gpio_value
            GPIOcallback(self.PIN)
            motionCallback.assert_called_with(next_state)

    def test_BadTransitions(self):
        motionCallback = Mock()
        ms = MotionSensor(self.PIN, motionCallback)
        ms.initialize()

        #Record GPIO callback method
        GPIOcallback=GPIO.add_event_detect.mock_calls[0][2]['callback']

        state_transition = [
            (1, True),  # Normal Transition
            (1, False), # Warning Transition (events were lost)
            (0, True),  # Normal Transition
            (0, False), # Warning Transition (events were lost)
        ]

        # Fake it .... till you make it ...
        for transition in state_transition:
            gpio_value = transition[0]
            should_call = transition[1]

            motionCallback.reset_mock()

            GPIO.input.return_value = gpio_value
            GPIOcallback(self.PIN)
            if should_call:
                motionCallback.assert_called()
            else:
                motionCallback.assert_not_called()
