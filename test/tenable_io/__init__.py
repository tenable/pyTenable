import unittest, os
from tenable.tenable_io import TenableIO

class APITest(unittest.TestCase):
    def setUp(self):
        self.api = TenableIO(
            os.environ['TIO_TEST_ADMIN_ACCESS'],
            os.environ['TIO_TEST_ADMIN_SECRET'])
        self.std = TenableIO(
            os.environ['TIO_TEST_STD_ACCESS'],
            os.environ['TIO_TEST_STD_SECRET']
        )

def suites():
    import agents

    return unittest.TestSuite([
        agents.suite(),
    ])