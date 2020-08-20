"""Entry point for the application."""
from routing.sensor_sink import SourceAndSink
from routing.mqtt_sender import MQTTSender
from routing.mqtt_subscriber import MQTTSubscriber

from sensors.BoschBME280.probe import ProbeBoschBME280
from sensors.BoschBME680.probe import ProbeBoschBME680
from sensors.TSL258x.probe import ProbeTSL258x
from sensors.RCWL0515.probe import ProbeRCWL0515

mqtt_subscriber = MQTTSubscriber()
mds = MQTTSender()
sender = [mds]

probefunctions = []
probefunctions.append(ProbeBoschBME280.probe)
probefunctions.append(ProbeBoschBME680.probe)
probefunctions.append(ProbeTSL258x.probe)
probefunctions.append(ProbeRCWL0515.probe)

sensor_types = []

for function in probefunctions:
    sensor_list = function(mds.send_payload)  # TODO: Send a more generic data sender callback.
    try:
        sensor_types += sensor_list
    except TypeError:
        pass

sensor_sink = SourceAndSink(sensor_types, sender)
sensor_sink.sink_and_send(3)
