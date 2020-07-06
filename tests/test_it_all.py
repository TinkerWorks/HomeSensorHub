from communication.sensor_hub import SensorHub
import unittest

class TestItAll(unittest.TestCase):
    def test_it_all(self):
        sensor_hub = SensorHub()
        sensor_hub.start_sniffin(interval=3)
