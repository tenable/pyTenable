import unittest
from datetime import datetime, timedelta
from test.tenable_io import APITest
from tenable.errors import *


class AgentExclusionsTests(APITest):
    def test_create(self):
        start = datetime.utcnow()
        end = datetime.utcnow() + timedelta(hours=1)

        with self.assertRaises(AttributeError):
            self.api.agents.exclusions.create('name')
        with self.assertRaises(TypeError):
            self.api.agents.exclusions.create('name',
                scanner_id='nope',
                start_time=start, 
                end_time=end)
        with self.assertRaises(TypeError):
            self.api.agents.exclusions.create(1.02,
                start_time=start, 
                end_time=end)
        with self.assertRaises(TypeError):
            self.api.agents.exclusions.create('name',
                start_time='nope', 
                end_time=end)
        with self.assertRaises(TypeError):
            self.api.agents.exclusions.create('name', 
                start_time=start,
                end_time='nope')
        with self.assertRaises(TypeError):
            self.api.agents.exclusions.create('name', 
                start_time=start, 
                end_time=end,
                timezone=1)
        with self.assertRaises(UnexpectedValueError):
            self.api.agents.exclusions.create('name', 
                start_time=start, 
                end_time=end,
                timezone='nonsense')
        with self.assertRaises(TypeError):
            self.api.agents.exclusions.create('name', 
                start_time=start, 
                end_time=end,
                description=True)
        with self.assertRaises(TypeError):
            self.api.agents.exclusions.create('name', 
                start_time=start, 
                end_time=end,
                frequency=1)
        with self.assertRaises(UnexpectedValueError):
            self.api.agents.exclusions.create('name', 
                start_time=start, 
                end_time=end,
                frequency='nope')
        with self.assertRaises(TypeError):
            self.api.agents.exclusions.create('name', 
                start_time=start, 
                end_time=end,
                interval='nope')
        with self.assertRaises(TypeError):
            self.api.agents.exclusions.create('name', 
                start_time=start, 
                end_time=end,
                frequency='weekly', 
                weekdays='nope')
        with self.assertRaises(UnexpectedValueError):
            self.api.agents.exclusions.create('name', 
                start_time=start, 
                end_time=end,
                frequency='weekly', 
                weekdays=['SU', 'MO', 'nope'])
        with self.assertRaises(TypeError):
            self.api.agents.exclusions.create('name',
                start_time=start, 
                end_time=end,
                frequency='monthly', 
                day_of_month='nope')
        with self.assertRaises(UnexpectedValueError):
            self.api.agents.exclusions.create('name',
                start_time=start, 
                end_time=end,
                frequency='monthly', 
                day_of_month=0)

        # Testing a one-time exclusion
        onetime = self.api.agents.exclusions.create('Test ONETIME', 
                    start_time=start,
                    end_time=end)
        self.assertTrue(isinstance(onetime, dict))
        self.api.agents.exclusions.delete(onetime['id'])

        # Testing a daily exclusion
        daily = self.api.agents.exclusions.create('Test DAILY',
                    start_time=start,
                    end_time=end,
                    frequency='daily')
        self.assertTrue(isinstance(daily, dict))
        self.api.agents.exclusions.delete(daily['id'])

        # Testing a weekly exclusion
        weekly = self.api.agents.exclusions.create('Test WEEKLY',
                    start_time=start,
                    end_time=end,
                    frequency='weekly',
                    weekdays=['MO', 'WE', 'FR'])
        self.assertTrue(isinstance(weekly, dict))
        self.api.agents.exclusions.delete(weekly['id'])

        # Testing a monthly exclusion
        monthly = self.api.agents.exclusions.create('Test MONTHLY',
                    start_time=start,
                    end_time=end,
                    frequency='monthly',
                    day_of_month=15)
        self.assertTrue(isinstance(monthly, dict))
        self.api.agents.exclusions.delete(monthly['id'])

        # Testing a yearly exclusion
        yearly = self.api.agents.exclusions.create('Test YEARLY',
                    start_time=start,
                    end_time=end,
                    frequency='yearly')
        self.assertTrue(isinstance(yearly, dict))
        self.api.agents.exclusions.delete(yearly['id'])

        # Standard users should not be able to create exceptions
        with self.assertRaises(PermissionError):
            self.std.agents.exclusions.create('Test STD ONETIME',
                start_time=start,
                end_time=end)

    def test_delete(self):
        with self.assertRaises(NotFoundError):
            self.api.agents.exclusions.delete(123)

        # Generating an exclusion for the purposes of further testing.
        excl = self.api.agents.exclusions.create('Test DELETION', 
                start_time=datetime.utcnow(),
                end_time=datetime.utcnow() + timedelta(hours=1))

        # Standard users should not be able to delete exclusions
        with self.assertRaises(PermissionError):
            self.std.agents.exclusions.delete(excl['id'])

        # Now to delete the exclusion
        self.api.agents.exclusions.delete(excl['id'])

    def test_details(self):
        with self.assertRaises(TypeError):
            self.api.agents.config.details(scanner_id='nope')
        self.assertTrue(isinstance(
            self.api.agents.config.details(), dict))

    def test_edit(self):
        # Create the Exclusion for the purposes of further testing.
        excl = self.api.agents.exclusions.create('Test EDIT', 
                start_time=datetime.utcnow(),
                end_time=datetime.utcnow() + timedelta(hours=1))

        with self.assertRaises(TypeError):
            self.api.agents.exclusions.edit()
        with self.assertRaises(TypeError):
            self.api.agents.exclusions.edit('nope')
        with self.assertRaises(TypeError):
            self.api.agents.exclusions.edit(excl['id'], scanner_id='nope')
        with self.assertRaises(TypeError):
            self.api.agents.exclusions.edit(excl['id'], name=1.02)
        with self.assertRaises(TypeError):
            self.api.agents.exclusions.edit(excl['id'], start_time='nope')
        with self.assertRaises(TypeError):
            self.api.agents.exclusions.edit(excl['id'], end_time='nope')
        with self.assertRaises(TypeError):
            self.api.agents.exclusions.edit(excl['id'], timezone=1)
        with self.assertRaises(UnexpectedValueError):
            self.api.agents.exclusions.edit(excl['id'], timezone='nonsense')
        with self.assertRaises(TypeError):
            self.api.agents.exclusions.edit(excl['id'], description=True)
        with self.assertRaises(TypeError):
            self.api.agents.exclusions.edit(excl['id'], frequency=1)
        with self.assertRaises(UnexpectedValueError):
            self.api.agents.exclusions.edit(excl['id'], frequency='nope')
        with self.assertRaises(TypeError):
            self.api.agents.exclusions.edit(excl['id'], interval='nope')
        with self.assertRaises(TypeError):
            self.api.agents.exclusions.edit(excl['id'], weekdays='nope')
        with self.assertRaises(UnexpectedValueError):
            self.api.agents.exclusions.edit(excl['id'], weekdays=['SU', 'MO', 'nope'])
        with self.assertRaises(TypeError):
            self.api.agents.exclusions.edit(excl['id'], day_of_month='nope')
        with self.assertRaises(UnexpectedValueError):
            self.api.agents.exclusions.edit(excl['id'], day_of_month=0)

        # Standard users cannot modify exclusions
        with self.assertRaises(PermissionError):
            self.std.agents.exclusions.edit(excl['id'], 
                name='Standard User EDIT')

        self.api.agents.exclusions.edit(excl['id'], name='Admin EDIT')
        self.api.agents.exclusions.delete(excl['id'])

    def test_list(self):
        # Create the Exclusion for the purposes of further testing.
        excl = self.api.agents.exclusions.create('Test LIST', 
                start_time=datetime.utcnow(),
                end_time=datetime.utcnow() + timedelta(hours=1))
        items = self.api.agents.exclusions.list()
        self.assertTrue(isinstance(items, list))
        self.assertTrue(excl in items)
        self.api.agents.exclusions.delete(excl['id'])


def suite():
    suite = unittest.TestSuite()
    suite.addTest(AgentExclusionsTests('test_create'))
    suite.addTest(AgentExclusionsTests('test_delete'))
    suite.addTest(AgentExclusionsTests('test_details'))
    suite.addTest(AgentExclusionsTests('test_edit'))
    suite.addTest(AgentExclusionsTests('test_list'))
    return suite