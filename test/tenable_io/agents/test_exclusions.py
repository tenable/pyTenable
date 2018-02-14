import unittest
from datetime import datetime, timedelta
from test.tenable_io.base import APITest
from tenable.errors import *


class AgentExclusionsTests(APITest):
    def test_create(self):
        start = datetime.utcnow()
        end = datetime.utcnow() + timedelta(hours=1)

        with self.assertRaises(AttributeError):
            self.api.agents.exclusions.create(1, 'name')
        with self.assertRaises(TypeError):
            self.api.agents.exclusions.create('nope', 'name',
                start_time=start, 
                end_time=end)
        with self.assertRaises(TypeError):
            self.api.agents.exclusions.create(1, 1.02,
                start_time=start, 
                end_time=end)
        with self.assertRaises(TypeError):
            self.api.agents.exclusions.create(1, 'name',
                start_time='nope', 
                end_time=end)
        with self.assertRaises(TypeError):
            self.api.agents.exclusions.create(1, 'name', 
                start_time=start,
                end_time='nope')
        # Timezone checking hasn't been implimented yet.
        #with self.assertRaises(TypeError):
        #    self.api.agents.exclusions.create(1, 'name', 
        #        start_time=start, 
        #        end_time=end,
        #        timezone='nope')
        with self.assertRaises(TypeError):
            self.api.agents.exclusions.create(1, 'name', 
                start_time=start, 
                end_time=end,
                description=True)
        with self.assertRaises(TypeError):
            self.api.agents.exclusions.create(1, 'name', 
                start_time=start, 
                end_time=end,
                frequency=1)
        with self.assertRaises(UnexpectedValueError):
            self.api.agents.exclusions.create(1, 'name', 
                start_time=start, 
                end_time=end,
                frequency='nope')
        with self.assertRaises(TypeError):
            self.api.agents.exclusions.create(1, 'name', 
                start_time=start, 
                end_time=end,
                interval='nope')
        with self.assertRaises(TypeError):
            self.api.agents.exclusions.create(1, 'name', 
                start_time=start, 
                end_time=end,
                frequency='weekly', 
                weekdays='nope')
        with self.assertRaises(UnexpectedValueError):
            self.api.agents.exclusions.create(1, 'name', 
                start_time=start, 
                end_time=end,
                frequency='weekly', 
                weekdays=['SU', 'MO', 'nope'])
        with self.assertRaises(TypeError):
            self.api.agents.exclusions.create(1, 'name',
                start_time=start, 
                end_time=end,
                frequency='monthly', 
                day_of_month='nope')
        with self.assertRaises(UnexpectedValueError):
            self.api.agents.exclusions.create(1, 'name',
                start_time=start, 
                end_time=end,
                frequency='monthly', 
                day_of_month=0)

        # Testing a one-time exclusion
        onetime = self.api.agents.exclusions.create(1, 'Test ONETIME', 
                    start_time=start,
                    end_time=end)
        self.assertTrue(isinstance(onetime, dict))
        self.api.agents.exclusions.delete(1, onetime['id'])

        # Testing a daily exclusion
        daily = self.api.agents.exclusions.create(1, 'Test DAILY',
                    start_time=start,
                    end_time=end,
                    frequency='daily')
        self.assertTrue(isinstance(daily, dict))
        self.api.agents.exclusions.delete(1, daily['id'])

        # Testing a weekly exclusion
        weekly = self.api.agents.exclusions.create(1, 'Test WEEKLY',
                    start_time=start,
                    end_time=end,
                    frequency='weekly',
                    weekdays=['MO', 'WE', 'FR'])
        self.assertTrue(isinstance(weekly, dict))
        self.api.agents.exclusions.delete(1, weekly['id'])

        # Testing a monthly exclusion
        monthly = self.api.agents.exclusions.create(1, 'Test MONTHLY',
                    start_time=start,
                    end_time=end,
                    frequency='monthly',
                    day_of_month=15)
        self.assertTrue(isinstance(monthly, dict))
        self.api.agents.exclusions.delete(1, monthly['id'])

        # Testing a yearly exclusion
        yearly = self.api.agents.exclusions.create(1, 'Test YEARLY',
                    start_time=start,
                    end_time=end,
                    frequency='yearly')
        self.assertTrue(isinstance(yearly, dict))
        self.api.agents.exclusions.delete(1, yearly['id'])

        # Standard users should not be able to create exceptions
        with self.assertRaises(PermissionError):
            self.std.agents.exclusions.create(1, 'Test STD ONETIME',
                start_time=start,
                end_time=end)


    def test_details(self):
        with self.assertRaises(TypeError):
            self.api.agents.config.details(scanner_id='nope')
        self.assertTrue(isinstance(
            self.api.agents.config.details(1), dict))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(AgentExclusionsTests('test_create'))
    return suite