"""Entry point for the application."""
from routing.sensor_sink import SourceAndSink
from routing.data_sender import DataSender
from sensors.probes.probe_BoschBME280 import ProbeBoschBME280
from sensors.probes.probe_BoschBME680 import ProbeBoschBME680
from sensors.probes.probe_TSL258x import ProbeTSL258x

probefunctions = [ProbeBoschBME280.probe,  ProbeBoschBME680.probe, ProbeTSL258x.probe]

sensor_types = []

for function in probefunctions:
    sensor_list = function()
    try:
        sensor_types += sensor_list
    except TypeError as e:
        pass

sender = [DataSender()]

sensor_sink = SourceAndSink(sensor_types, sender)
sensor_sink.sink_and_send(3)
