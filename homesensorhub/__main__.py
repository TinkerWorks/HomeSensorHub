"""Entry point for the application."""
from routing.sensor_sink import SourceAndSink
from routing.data_sender import DataSender
from sensors.probes.probe_BoschBME280 import ProbeAdafruitBME280
from sensors.probes.probe_TSL258x import ProbeTSL258x

sensor_types_BoschBME280 = ProbeAdafruitBME280.probe()
sensor_types_TSL258x = ProbeTSL258x.probe()

sensor_types = sensor_types_BoschBME280 + \
               sensor_types_TSL258x
sender = [DataSender()]

sensor_sink = SourceAndSink(sensor_types, sender)
sensor_sink.sink_and_send(3)
