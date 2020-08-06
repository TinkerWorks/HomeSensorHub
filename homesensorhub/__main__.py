"""Entry point for the application."""
from routing.sensor_sink import SourceAndSink
from routing.data_sender import DataSender
from sensors.environmental_sensor import EnvironmentalSensorProbe
from sensors.light_sensor import LightSensorProbe

sensors = [EnvironmentalSensorProbe(),
           LightSensorProbe()]
sender = [DataSender()]

sensor_sink = SourceAndSink(sensors, sender)
sensor_sink.sink_and_send(3)
