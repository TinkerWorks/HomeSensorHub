import unittest
import subprocess
import time
import signal


class TestMain(unittest.TestCase):

    TIMEOUT_SECONDS = 30
    POLL_INTERVAL_SECONDS=0.1

    START_STOP_DURATION_SECONDS=5

    def test_start_stop(self):
        """Test that main runs for five seconds without crashing."""
        proc = subprocess.Popen(["/usr/bin/python3", "homesensorhub/__main__.py"])
        time.sleep(self.START_STOP_DURATION_SECONDS)
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
        self.assertEqual(0, proc.returncode)
