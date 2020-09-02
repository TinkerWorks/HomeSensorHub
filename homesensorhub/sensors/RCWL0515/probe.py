#!/usr/bin/env python3

"""Module which contains sketch the probing the BoschBME sensors."""
from sensors.probe import Probe
from sensors.RCWL0515.driver import MotionSensorRCWL0515


class ProbeRCWL0515(Probe):
    """Class which implements probing for BoschBME sensors."""

    # This should come from a settings file (read-only prefferably)
    GPIO = 4  # BCM notation for GPIO 7

    @classmethod
    def probe(cls, send_payload_callback=None) -> list:
        """
        Probe for Bosch BME type sensors to the possible I2C addresses.

        Function which iterates over multiple I2C addresses and look for
        sensors of the type BoschBME. In case the sensor is not found at any
        of the specified I2C address, None is returned.
        """
        return [MotionSensorRCWL0515(gpio=cls.GPIO, pollrate=1, callback=send_payload_callback)]
