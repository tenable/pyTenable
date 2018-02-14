import unittest
from test.tenable_io.base import APITest
from tenable.errors import *


class AgentConfigTests(APITest):
    def test_edit(self):
        with self.assertRaises(TypeError):
            self.api.agents.config.edit('nope')
        with self.assertRaises(TypeError):
            self.api.agents.config.edit(1, software_update='nope')
        with self.assertRaises(TypeError):
            self.api.agents.config.edit(1, auto_unlink='nope')
        with self.assertRaises(UnexpectedValueError):
            self.api.agents.config.edit(1, auto_unlink=500)
        self.assertTrue(isinstance(
            self.api.agents.config.edit(1, auto_unlink=30), dict))
        self.assertTrue(isinstance(
            self.api.agents.config.edit(1, auto_unlink=False), dict))

    def test_details(self):
        with self.assertRaises(TypeError):
            self.api.agents.config.details(scanner_id='nope')
        self.assertTrue(isinstance(
            self.api.agents.config.details(1), dict))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(AgentConfigTests('test_edit'))
    suite.addTest(AgentConfigTests('test_details'))
    return suite