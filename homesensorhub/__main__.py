"""Entry point for the application."""
from routing.sensor_sink import SourceAndSink
from routing.data_sender import DataSender
from sensors.BoschBME280.probe import ProbeBoschBME280
from sensors.BoschBME680.probe import ProbeBoschBME680
from sensors.TSL258x.probe import ProbeTSL258x

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
