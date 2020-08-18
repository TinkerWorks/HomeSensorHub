#!/usr/bin/env python3

"""Module which contains sketch the probing the BoschBME sensors."""
from sensors.probes.probe import Probe
from sensors.types.RCWL0515.MotionSensorRCWL0515 import MotionSensorRCWL0515

import logging

logging.basicConfig(level=logging.INFO)


class ProbeRCWL0515(Probe):
    """Class which implements probing for BoschBME sensors."""

    # This should come from a settings file (read-only prefferably)
    GPIO = 4 # BCM notation for GPIO 7

    @classmethod
    def probe(cls) -> list:
        """
        Probe for Bosch BME type sensors to the possible I2C addresses.

        Function which iterates over multiple I2C addresses and look for
        sensors of the type BoschBME. In case the sensor is not found at any
        of the specified I2C address, None is returned.
        """

        return MotionSensorRCWL0515(gpio=cls.GPIO)
