import unittest
import subprocess


class TestMain(unittest.TestCase):

    def test_main(self):
        subprocess.call(["/usr/bin/python3", "homesensorhub/__main__.py"])
