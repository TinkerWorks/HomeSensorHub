"""Entry point for the application."""
from communication.sensor_sink import SensorSink

if __name__ == "__main__":
    sensor_sink = SensorSink()
    sensor_sink.sink_and_send(3)
