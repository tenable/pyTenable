import unittest
import config
import exclusions


def suite():
    return unittest.TestSuite([
        config.suite(),
        exclusions.suite(),
    ])