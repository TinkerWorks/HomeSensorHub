#!/bin/env python3
import datetime
import logging

from time import sleep
import RPi.GPIO as GPIO


class MotionSensor:
    ms_dict = {}

    def __init__(self, gpio=7, callback=None):
        self.logger = logging.getLogger(__name__)
        self.MOTION_GPIO = gpio
        self.callback = callback

        # Read initial state
        self.motion = None
        self.__motionChanged(self.MOTION_GPIO)

    def get(self):
        return self.motion

    def initialize(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.MOTION_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        MotionSensor.ms_dict[self.MOTION_GPIO] = self
        GPIO.add_event_detect(self.MOTION_GPIO, GPIO.BOTH,
                              callback=MotionSensor.__motionChangedStatic)

    def __motionChangedStatic(gpio):
        MotionSensor.ms_dict[gpio].__motionChanged(gpio)

    def __motionChanged(self, gpio):
        if GPIO.input(self.MOTION_GPIO):
            next_motion = True
            self.logger.debug("Motion Started %d" % gpio)
        else:
            next_motion = False
            self.logger.debug("Motion Ended %d" % gpio)

        if(next_motion == self.motion):
            self.logger.error("Motion Transitioned from {} to {}".format(self.motion, next_motion))
        else:
            self.motion = next_motion

            if(self.callback is not None):
                self.callback(self.motion)
