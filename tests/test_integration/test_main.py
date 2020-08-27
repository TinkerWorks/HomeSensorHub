import unittest
import subprocess
import time
import signal
import paho.mqtt.client as mqtt
import getpass
import socket


class TestMain(unittest.TestCase):

    TIMEOUT_SECONDS = 3
    POLL_INTERVAL_SECONDS = 0.1

    START_STOP_DURATION_MAX_SECONDS = 4
    START_STOP_COUNT = 8

    RUNTIME = 5

    def start_stop(self, callback, allowed_rc=[0]):
        """Test that main runs for five seconds without crashing."""
        proc = subprocess.Popen(["/usr/bin/python3", "homesensorhub/__main__.py"])
        print("Running status is:", proc.poll())
        callback(proc)
        print("Running status is:", proc.poll())
        proc.send_signal(signal.SIGINT)

        timeout = self.TIMEOUT_SECONDS
        while proc.poll() is None and timeout >= 0:
            print("Wait to finish poll rc is ", proc.poll())
            time.sleep(self.POLL_INTERVAL_SECONDS)
            timeout -= self.POLL_INTERVAL_SECONDS

        if not proc.poll():
            proc.send_signal(signal.SIGKILL)

        timeout = self.TIMEOUT_SECONDS
        while proc.poll() is None and timeout >= 0:
            print("Wait to finish poll rc is ", proc.poll())
            time.sleep(self.POLL_INTERVAL_SECONDS)
            timeout -= self.POLL_INTERVAL_SECONDS

        print("Finish poll rc is ", proc.poll())
        self.assertIn(proc.returncode, allowed_rc)

    def connect_mqtt(self):
        client = mqtt.Client()
        client.connect("mqtt.tinker.haus", 1883)
        return client

    def on_message(self, client, userdata, message):
        print("Received message '" + str(message.payload) + "' on topic '"
              + message.topic + "' with QoS " + str(message.qos))

    def test_1_runtime(self):
        def cb(proc):
            print("LISTENIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIING")
            client = self.connect_mqtt()
            client.on_message = self.on_message

            topic_prefix = getpass.getuser() + "/" + socket.gethostname()
            topic = topic_prefix + "/temperature/value"
            r = client.subscribe(topic)

            print(r)

            rt = self.RUNTIME
            while rt > 0:
                client.loop(timeout=10)
                time.sleep(0.5)
                rt -= 0.5
            print("DOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONE")

        self.start_stop(cb)

    def test_0_start_stop_stress(self):
        duration = self.START_STOP_DURATION_MAX_SECONDS
        for i in range(0, self.START_STOP_COUNT):

            def cb(proc):
                print("Run for {} seconds".format(duration))
                time.sleep(duration)

            # Either normal, or keyboard interrupt stop
            # TODO: or sometimes a kill (this should not happen)
            rc = [0, 1, -signal.SIGINT, -signal.SIGKILL]
            self.start_stop(cb, rc)
            duration -= self.START_STOP_DURATION_MAX_SECONDS / self.START_STOP_COUNT
