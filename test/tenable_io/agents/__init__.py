import unittest
import test_config
import test_exclusions


def suite():
    return unittest.TestSuite([
        test_config.suite(),
        test_exclusions.suite(),
    ])