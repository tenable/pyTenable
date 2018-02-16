import tenable_io
import securitycenter
import unittest

def run_all():
    suites = unittest.TestSuite([
        tenable_io.suites(),
        securitycenter.suites(),
    ])
    unittest.TextTestRunner(verbosity=2).run(suites)


def run_tenable_io():
    unittest.TextTestRunner(verbosity=2).run(tenable_io.suites())


def run_securitycenter():
    unittest.TextTestRunner(verbosity=2).run(securitycenter.suites())