import tenable_io
import securitycenter
import unittest

def run():
    suites = unittest.TestSuite([
        tenable_io.suites(),
    ])
    unittest.TextTestRunner(verbosity=2).run(suites)