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
    import agent_config
    import agent_exclusions
    import agent_groups

    return unittest.TestSuite([
        agent_config.suite(),
        agent_exclusions.suite(),
        agent_groups.suite(),
    ])