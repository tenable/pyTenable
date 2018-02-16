import unittest
from datetime import datetime, timedelta
from test.tenable_io import APITest
from tenable.errors import *


class AgentExclusionsTests(APITest):
    def test_create_agent_blackout_exclusion(self):
        start = datetime.utcnow()
        end = datetime.utcnow() + timedelta(hours=1)

        with self.assertRaises(AttributeError):
            self.api.agent_exclusions.create('name')
        with self.assertRaises(TypeError):
            self.api.agent_exclusions.create('name',
                scanner_id='nope',
                start_time=start, 
                end_time=end)
        with self.assertRaises(TypeError):
            self.api.agent_exclusions.create(1.02,
                start_time=start, 
                end_time=end)
        with self.assertRaises(TypeError):
            self.api.agent_exclusions.create('name',
                start_time='nope', 
                end_time=end)
        with self.assertRaises(TypeError):
            self.api.agent_exclusions.create('name', 
                start_time=start,
                end_time='nope')
        with self.assertRaises(TypeError):
            self.api.agent_exclusions.create('name', 
                start_time=start, 
                end_time=end,
                timezone=1)
        with self.assertRaises(UnexpectedValueError):
            self.api.agent_exclusions.create('name', 
                start_time=start, 
                end_time=end,
                timezone='nonsense')
        with self.assertRaises(TypeError):
            self.api.agent_exclusions.create('name', 
                start_time=start, 
                end_time=end,
                description=True)
        with self.assertRaises(TypeError):
            self.api.agent_exclusions.create('name', 
                start_time=start, 
                end_time=end,
                frequency=1)
        with self.assertRaises(UnexpectedValueError):
            self.api.agent_exclusions.create('name', 
                start_time=start, 
                end_time=end,
                frequency='nope')
        with self.assertRaises(TypeError):
            self.api.agent_exclusions.create('name', 
                start_time=start, 
                end_time=end,
                interval='nope')
        with self.assertRaises(TypeError):
            self.api.agent_exclusions.create('name', 
                start_time=start, 
                end_time=end,
                frequency='weekly', 
                weekdays='nope')
        with self.assertRaises(UnexpectedValueError):
            self.api.agent_exclusions.create('name', 
                start_time=start, 
                end_time=end,
                frequency='weekly', 
                weekdays=['SU', 'MO', 'nope'])
        with self.assertRaises(TypeError):
            self.api.agent_exclusions.create('name',
                start_time=start, 
                end_time=end,
                frequency='monthly', 
                day_of_month='nope')
        with self.assertRaises(UnexpectedValueError):
            self.api.agent_exclusions.create('name',
                start_time=start, 
                end_time=end,
                frequency='monthly', 
                day_of_month=0)

        # Testing a one-time exclusion
        onetime = self.api.agent_exclusions.create('Test ONETIME', 
                    start_time=start,
                    end_time=end)
        self.assertTrue(isinstance(onetime, dict))
        self.api.agent_exclusions.delete(onetime['id'])

        # Testing a daily exclusion
        daily = self.api.agent_exclusions.create('Test DAILY',
                    start_time=start,
                    end_time=end,
                    frequency='daily')
        self.assertTrue(isinstance(daily, dict))
        self.api.agent_exclusions.delete(daily['id'])

        # Testing a weekly exclusion
        weekly = self.api.agent_exclusions.create('Test WEEKLY',
                    start_time=start,
                    end_time=end,
                    frequency='weekly',
                    weekdays=['MO', 'WE', 'FR'])
        self.assertTrue(isinstance(weekly, dict))
        self.api.agent_exclusions.delete(weekly['id'])

        # Testing a monthly exclusion
        monthly = self.api.agent_exclusions.create('Test MONTHLY',
                    start_time=start,
                    end_time=end,
                    frequency='monthly',
                    day_of_month=15)
        self.assertTrue(isinstance(monthly, dict))
        self.api.agent_exclusions.delete(monthly['id'])

        # Testing a yearly exclusion
        yearly = self.api.agent_exclusions.create('Test YEARLY',
                    start_time=start,
                    end_time=end,
                    frequency='yearly')
        self.assertTrue(isinstance(yearly, dict))
        self.api.agent_exclusions.delete(yearly['id'])

        # Standard users should not be able to create exceptions
        with self.assertRaises(PermissionError):
            self.std.agent_exclusions.create('Test STD ONETIME',
                start_time=start,
                end_time=end)

    def test_delete_agent_blackout_exclusion(self):
        with self.assertRaises(NotFoundError):
            self.api.agent_exclusions.delete(123)

        # Generating an exclusion for the purposes of further testing.
        excl = self.api.agent_exclusions.create('Test DELETION', 
                start_time=datetime.utcnow(),
                end_time=datetime.utcnow() + timedelta(hours=1))

        # Standard users should not be able to delete exclusions
        with self.assertRaises(PermissionError):
            self.std.agent_exclusions.delete(excl['id'])

        # Now to delete the exclusion
        self.api.agent_exclusions.delete(excl['id'])

    def test_agent_blackout_exclusion_details(self):
        with self.assertRaises(TypeError):
            self.api.agent_exclusions.details(scanner_id='nope')
        with self.assertRaises(TypeError):
            self.api.agent_exclusions.details('nope')

        excl = self.api.agent_exclusions.create('Test LIST', 
                start_time=datetime.utcnow(),
                end_time=datetime.utcnow() + timedelta(hours=1))
        check = self.api.agent_exclusions.details(excl['id'])

        self.assertTrue(excl['id'] == check['id'])
        self.assertTrue(excl['name'] == check['name'])
        self.api.agent_exclusions.delete(excl['id'])

    def test_edit_agent_blackout_exclusion(self):
        # Create the Exclusion for the purposes of further testing.
        excl = self.api.agent_exclusions.create('Test EDIT', 
                start_time=datetime.utcnow(),
                end_time=datetime.utcnow() + timedelta(hours=1))

        with self.assertRaises(TypeError):
            self.api.agent_exclusions.edit()
        with self.assertRaises(TypeError):
            self.api.agent_exclusions.edit('nope')
        with self.assertRaises(TypeError):
            self.api.agent_exclusions.edit(excl['id'], scanner_id='nope')
        with self.assertRaises(TypeError):
            self.api.agent_exclusions.edit(excl['id'], name=1.02)
        with self.assertRaises(TypeError):
            self.api.agent_exclusions.edit(excl['id'], start_time='nope')
        with self.assertRaises(TypeError):
            self.api.agent_exclusions.edit(excl['id'], end_time='nope')
        with self.assertRaises(TypeError):
            self.api.agent_exclusions.edit(excl['id'], timezone=1)
        with self.assertRaises(UnexpectedValueError):
            self.api.agent_exclusions.edit(excl['id'], timezone='nonsense')
        with self.assertRaises(TypeError):
            self.api.agent_exclusions.edit(excl['id'], description=True)
        with self.assertRaises(TypeError):
            self.api.agent_exclusions.edit(excl['id'], frequency=1)
        with self.assertRaises(UnexpectedValueError):
            self.api.agent_exclusions.edit(excl['id'], frequency='nope')
        with self.assertRaises(TypeError):
            self.api.agent_exclusions.edit(excl['id'], interval='nope')
        with self.assertRaises(TypeError):
            self.api.agent_exclusions.edit(excl['id'], weekdays='nope')
        with self.assertRaises(UnexpectedValueError):
            self.api.agent_exclusions.edit(excl['id'], weekdays=['SU', 'MO', 'nope'])
        with self.assertRaises(TypeError):
            self.api.agent_exclusions.edit(excl['id'], day_of_month='nope')
        with self.assertRaises(UnexpectedValueError):
            self.api.agent_exclusions.edit(excl['id'], day_of_month=0)

        # Standard users cannot modify exclusions
        with self.assertRaises(PermissionError):
            self.std.agent_exclusions.edit(excl['id'], 
                name='Standard User EDIT')

        self.api.agent_exclusions.edit(excl['id'], name='Admin EDIT')
        self.api.agent_exclusions.delete(excl['id'])

    def test_list_agent_blackout_exclusions(self):
        # Create the Exclusion for the purposes of further testing.
        excl = self.api.agent_exclusions.create('Test LIST', 
                start_time=datetime.utcnow(),
                end_time=datetime.utcnow() + timedelta(hours=1))
        items = self.api.agent_exclusions.list()
        self.assertTrue(isinstance(items, list))
        self.assertTrue(excl in items)
        self.api.agent_exclusions.delete(excl['id'])


def suite():
    suite = unittest.TestSuite()
    suite.addTest(AgentExclusionsTests('test_create_agent_blackout_exclusion'))
    suite.addTest(AgentExclusionsTests('test_delete_agent_blackout_exclusion'))
    suite.addTest(AgentExclusionsTests('test_agent_blackout_exclusion_details'))
    suite.addTest(AgentExclusionsTests('test_edit_agent_blackout_exclusion'))
    suite.addTest(AgentExclusionsTests('test_list_agent_blackout_exclusions'))
    return suite