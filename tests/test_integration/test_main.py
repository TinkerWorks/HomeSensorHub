import unittest
import subprocess
import time
import signal


class TestMain(unittest.TestCase):

    def test_main(self):
        proc = subprocess.Popen(["/usr/bin/python3", "homesensorhub/__main__.py"])
        time.sleep(5)
        proc.send_signal(signal.SIGINT)
