from .base import all_suites
import unittest

def run_tests():
    unittest.TextTestRunner(verbosity=2).run(all_suites())