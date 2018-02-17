import unittest
from test.tenable_io import APITest
from tenable.errors import *


class AgentGroupTests(APITest):
    def test_add_agent_to_group(self):
        with self.assertRaises(TypeError):
            self.api.agent_groups.add_agent('nope', 1)
        with self.assertRaises(TypeError):
            self.api.agent_groups.add_agent(1, 'nope')
        with self.assertRaises(TypeError):
            self.api.agent_groups.add_agent(1, 1, scanner_id='nope')

        with self.assertRaises(NotFoundError):
            self.api.agent_groups.add_agent(1, 1)

        with self.assertRaises(PermissionError):
            self.std.agent_groups.add_agent(1, 1)

        ### Need to get a mock agent to test this further

    def test_configure_agent_group(self):
        with self.assertRaises(TypeError):
            self.api.agent_groups.configure('nope', 1, 'something')
        with self.assertRaises(TypeError):
            self.api.agent_groups.configure(1, 'nope', 'something')
        with self.assertRaises(TypeError):
            self.api.agent_groups.configure(1, 1, 1)
        with self.assertRaises(TypeError):
            self.api.agent_groups.configure(1, 1, 'something', scanner_id='nope')

        group = self.api.agent_groups.create('Example TEST CONFIGURE')

        with self.assertRaises(PermissionError):
            self.std.agent_groups.configure(group['id'], 'STD USER TEST')

        modded = self.api.agent_groups.configure(group['id'], 'RECONFIGURED TEST')
        self.assertTrue(group['id'] == modded['id'])
        self.assertTrue(modded['name'] == 'RECONFIGURED TEST')
        self.api.agent_groups.delete(group['id'])

    def test_create_new_agent_group(self):
        with self.assertRaises(TypeError):
            self.api.agent_groups.create(1)
        with self.assertRaises(TypeError):
            self.api.agent_groups.create('something', 'nope')

        with self.assertRaises(PermissionError):
            self.std.agent_groups.create('Example STD USER CREATE')

        group = self.api.agent_groups.create('Example TEST CREATE')
        self.api.agent_groups.delete(group['id'])

    def test_delete_agent_group(self):
        with self.assertRaises(TypeError):
            self.api.agent_groups.delete('nope')
        with self.assertRaises(TypeError):
            self.api.agent_groups.delete(1, scanner_id='nope')

        group = self.api.agent_groups.create('Example TEST DELETE')

        with self.assertRaises(PermissionError):
            self.std.agent_groups.delete(group['id'])

        self.api.agent_groups.delete(group['id'])

    def test_delete_agent_from_group(self):
        with self.assertRaises(TypeError):
            self.api.agent_groups.delete_agent('nope', 1)
        with self.assertRaises(TypeError):
            self.api.agent_groups.delete_agent(1, 'nope')
        with self.assertRaises(TypeError):
            self.api.agent_groups.delete_agent(1, 1, scanner_id='nope')

        with self.assertRaises(NotFoundError):
            self.api.agent_groups.delete_agent(1, 1)

        with self.assertRaises(PermissionError):
            self.std.agent_groups.delete_agent(1, 1)

        ### Need to get a mock agent to test this further

    def test_agent_group_details(self):
        with self.assertRaises(TypeError):
            self.api.agent_groups.details('nope')
        with self.assertRaises(TypeError):
            self.api.agent_groups.details(1, scanner_id='nope')

        # Instead of a 404 error, passing a non-existent agent-group ID seems
        # to throw a 500 error.
        #with self.assertRaises(NotFoundError):
        #    self.api.agent_groups.details(999999)

        #with self.assertRaises(PermissionError):
        #    self.api.agent_groups.details(999999)
        with self.assertRaises(ServerError):
            self.api.agent_groups.details(999999)

        group = self.api.agent_groups.create('Example DETAIL TEST')
        detail = self.api.agent_groups.details(group['id'])

        self.assertTrue(group['name'] == detail['name'])
        self.api.agent_groups.delete(group['id'])


def suite():
    suite = unittest.TestSuite()
    suite.addTest(AgentGroupTests('test_add_agent_to_group'))
    suite.addTest(AgentGroupTests('test_configure_agent_group'))
    suite.addTest(AgentGroupTests('test_delete_agent_group'))
    suite.addTest(AgentGroupTests('test_delete_agent_from_group'))
    suite.addTest(AgentGroupTests('test_agent_group_details'))
    return suite