from communication.sensor_sink import SensorSink
import unittest

class TestItAll(unittest.TestCase):
    def test_it_all(self):
        sensor_sink = SensorSink()
        sensor_sink.sink(interval=3)
