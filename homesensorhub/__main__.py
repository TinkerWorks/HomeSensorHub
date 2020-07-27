"""Entry point for the application."""
from communication.sensor_sink import SensorSink


sensor_sink = SensorSink()
sensor_sink.sink_and_send(3)
