import unittest
import subprocess
import time
import signal


class TestMain(unittest.TestCase):

    TIMEOUT = 30

    def test_main(self):
        """Test that main runs for five seconds without crashing."""
        proc = subprocess.Popen(["/usr/bin/python3", "homesensorhub/__main__.py"])
        time.sleep(5)

        proc.send_signal(signal.SIGINT)
        timeout = self.TIMEOUT
        while proc.poll() is None and timeout >= 0:
            time.sleep(0.1)
            timeout -= 1

        if not proc.poll():
            proc.terminate()

        self.assertEqual(0, proc.returncode)
