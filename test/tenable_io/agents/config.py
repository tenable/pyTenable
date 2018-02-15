import unittest
from test.tenable_io import APITest
from tenable.errors import *


class AgentConfigTests(APITest):
    def test_edit(self):
        with self.assertRaises(TypeError):
            self.api.agents.config.edit('nope')
        with self.assertRaises(TypeError):
            self.api.agents.config.edit(software_update='nope')
        with self.assertRaises(TypeError):
            self.api.agents.config.edit(auto_unlink='nope')
        with self.assertRaises(UnexpectedValueError):
            self.api.agents.config.edit(auto_unlink=500)
        self.assertTrue(isinstance(
            self.api.agents.config.edit(auto_unlink=30), dict))
        self.assertTrue(isinstance(
            self.api.agents.config.edit(auto_unlink=False), dict))

    def test_details(self):
        with self.assertRaises(TypeError):
            self.api.agents.config.details(scanner_id='nope')
        self.assertTrue(isinstance(
            self.api.agents.config.details(), dict))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(AgentConfigTests('test_edit'))
    suite.addTest(AgentConfigTests('test_details'))
    return suite