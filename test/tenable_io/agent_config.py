import unittest
from test.tenable_io import APITest
from tenable.errors import *


class AgentConfigTests(APITest):
    def test_edit_agent_configuration(self):
        with self.assertRaises(TypeError):
            self.api.agent_config.edit('nope')
        with self.assertRaises(TypeError):
            self.api.agent_config.edit(software_update='nope')
        with self.assertRaises(TypeError):
            self.api.agent_config.edit(auto_unlink='nope')
        with self.assertRaises(UnexpectedValueError):
            self.api.agent_config.edit(auto_unlink=500)
        self.assertTrue(isinstance(
            self.api.agent_config.edit(auto_unlink=30), dict))
        self.assertTrue(isinstance(
            self.api.agent_config.edit(auto_unlink=False), dict))

    def test_show_agent_configuration_details(self):
        with self.assertRaises(TypeError):
            self.api.agent_config.details(scanner_id='nope')
        self.assertTrue(isinstance(
            self.api.agent_config.details(), dict))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(AgentConfigTests('test_edit_agent_configuration'))
    suite.addTest(AgentConfigTests('test_show_agent_configuration_details'))
    return suite