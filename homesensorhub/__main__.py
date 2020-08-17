"""Entry point for the application."""
from routing.sensor_sink import SourceAndSink
from routing.data_sender import DataSender
from sensors.probes.probe_BoschBME280 import ProbeAdafruitBME280

sensor_types_BoschBME280 = ProbeAdafruitBME280.probe()
sender = [DataSender()]

sensor_sink = SourceAndSink(sensor_types_BoschBME280, sender)
sensor_sink.sink_and_send(3)
