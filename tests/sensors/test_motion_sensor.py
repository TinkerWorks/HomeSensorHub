import sys

# TODO: This is a way, but overriding __import__ might be better
from mock import Mock
if 'RPi' not in sys.modules.keys():
    sys.modules['RPi'] = Mock()
if 'RPi.GPIO' not in sys.modules.keys():
    sys.modules['RPi.GPIO'] = Mock()

import RPi.GPIO as GPIO

from sensors.RCWL0515.driver import MotionSensorRCWL0515

import unittest


class MotionSensorTests(unittest.TestCase):

    PIN = 3

    def test_GetState(self):
        cases = {
            (0, False),
            (1, True),
        }

        for case in cases:
            gpio_value = case[0]
            get_value = case[1]

            GPIO.input.return_value = gpio_value
            motionCallback = Mock()
            ms = MotionSensorRCWL0515(self.PIN, callback=motionCallback)

            self.assertEqual(ms.get(), get_value)
            ms.stop()

    def test_NormalTransitions(self):
        # initial state is false
        GPIO.input.return_value = False

        motionCallback = Mock()
        ms = MotionSensorRCWL0515(self.PIN, callback=motionCallback)

        # Record GPIO callback method
        GPIOcallback = GPIO.add_event_detect.mock_calls[0][2]['callback']

        state_transition = [
            (1, True),
            (0, False),
            (1, True),
            (0, False),
        ]

        ms.stop()

        # Fake it .... till you make it ...
        for transition in state_transition:
            gpio_value = transition[0]
            next_state = transition[1]

            motionCallback.reset_mock()

            GPIO.input.return_value = gpio_value
            GPIOcallback(self.PIN)

            self.assertEqual(motionCallback.call_args.args[0].get_value(), next_state)

    def test_BadTransitions(self):
        # initial state is false
        GPIO.input.return_value = False

        motionCallback = Mock()
        ms = MotionSensorRCWL0515(self.PIN, callback=motionCallback)

        # Record GPIO callback method
        GPIOcallback = GPIO.add_event_detect.mock_calls[0][2]['callback']

        state_transition = [
            (1, True),   # Normal Transition
            (1, False),  # Warning Transition (events were lost)
            (0, True),   # Normal Transition
            (0, False),  # Warning Transition (events were lost)
        ]

        ms.stop()

        # Fake it .... till you make it ...
        for transition in state_transition:
            gpio_value = transition[0]

            motionCallback.reset_mock()

            GPIO.input.return_value = gpio_value
            GPIOcallback(self.PIN)
            motionCallback.assert_called()
