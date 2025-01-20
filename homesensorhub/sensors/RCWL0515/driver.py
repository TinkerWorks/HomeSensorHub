#!/usr/bin/env python3

import RPi.GPIO as GPIO

from homesensorhub.sensors.sensor_types import Motion
from homesensorhub.utils import logging


class MotionSensorRCWL0515(Motion):
    ms_dict = {}

    def __init__(self, gpio, callback=None):
        self.logger = logging.getLogger(__name__)
        self.MOTION_GPIO = gpio

        # Read initial state
        self.motion = None
        self.initialize_gpio()
        Motion.__init__(self, send_payload_callback=callback)
        self.__motionChanged(self.MOTION_GPIO)

        self.install_callback()

    def get_sensor_name(self):
        return "RCWL-0515"

    def __get_gpio_value(self):
        if GPIO.input(self.MOTION_GPIO):
            motion = True
        else:
            motion = False
        return motion

    def get_sensor_value(self):
        self.logger.debug("Motion value polled")

        next_motion = self.__get_gpio_value()
        if next_motion:
            self.logger.debug("Motion is in progress")
        else:
            self.logger.debug("Motion is not happening")

        if (next_motion != self.motion):
            self.logger.error("Motion from {} to {} (IRQ skip detected because of race condition)"
                              .format(self.motion, next_motion))

        self.motion = next_motion

        return self.motion

    def get_sensor_measure(self):
        return "None"

    def get(self):
        return self.get_sensor_value()

    def initialize_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.MOTION_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def install_callback(self):
        MotionSensorRCWL0515.ms_dict[self.MOTION_GPIO] = self
        GPIO.remove_event_detect(self.MOTION_GPIO)
        GPIO.add_event_detect(self.MOTION_GPIO, GPIO.BOTH,
                              callback=MotionSensorRCWL0515.__motionChangedStatic)

    def __motionChangedStatic(gpio):
        MotionSensorRCWL0515.ms_dict[gpio].__motionChanged(gpio)

    def __motionChanged(self, gpio):
        self.logger.debug("Motion Changed IRQ at GPIO %d" % gpio)
        next_motion = self.__get_gpio_value()
        if next_motion:
            self.logger.debug("Motion Started")
        else:
            self.logger.debug("Motion Ended")

        if (next_motion == self.motion):
            self.logger.error("Motion from {} to {} (IRQ skipped)"
                              .format(self.motion, next_motion))

        self.motion = next_motion

        if (self.send_payload_callback is not None):
            self.logger.debug("Will poll again from asynchronous callback : ....")
            self.send_payload_callback(self.get_payload())
