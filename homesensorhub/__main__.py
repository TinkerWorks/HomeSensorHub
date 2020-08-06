"""Entry point for the application."""
from communication.sensor_sink import SensorSink
from sensors.environmental_sensor import EnvironmentalSensorProbe
from sensors.light_sensor import LightSensorProbe

sensors = [EnvironmentalSensorProbe(),
           LightSensorProbe()]
sensor_sink = SensorSink(sensors)
sensor_sink.sink_and_send(3)
