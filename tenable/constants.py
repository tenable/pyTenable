from datetime import datetime, timedelta

class IOConstants:
    '''
    This class contains all the constants related to IO package
    '''

    class CaseConst:
        # for case parameter in check
        uppercase = 'upper'
        lowecase = 'lower'

    class ScheduleConst:
        '''
        This class contains common constants required for schedule
        '''
        # frequency type
        onetime = 'ONETIME'
        daily = 'DAILY'
        weekly = 'WEEKLY'
        monthly = 'MONTHLY'
        yearly = 'YEARLY'

        # frequency
        frequency = 'frequency'
        frequency_default = onetime
        frequency_choice = [onetime, daily, weekly, monthly, yearly]

        # frequency-WEEKLY
        weekdays = 'byweekday'
        weekdays_default = ['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA']

        # frequency-MONTHLY
        day_of_month = 'day_of_month'
        day_of_month_choice = list(range(1, 32))
        day_of_month_default = datetime.today().day

        # INTERVAL
        interval = 'interval'
        interval_default = 1

        # START-TIME
        start_time = 'starttime'
        start_time_default = datetime.utcnow()

        # END-TIME
        end_time = 'endtime'
        end_time_default = datetime.utcnow() + timedelta(hours=1)

        # TIMEZONE
        timezone = 'timezone'
        timezone_default = 'Etc/UTC'

        # rrule
        rrules = 'rrules'

    class ScanScheduleConst(ScheduleConst):
        '''
        This class inherits all variables from ScheduleConst and
        contains additional variables required for scan scheduling
        '''
        # formatting and comparison values required in scan schedule
        ffrequency = 'FREQ={}'
        finterval = 'INTERVAL={}'
        fbyweekday = 'BYDAY={}'
        fbymonthday = 'BYMONTHDAY={}'

        weekly_frequency = 'FREQ=WEEKLY'
        monthly_frequency = 'FREQ=MONTHLY'

        enabled = 'enabled'
        launch = 'launch'
        schedule_scan = 'scheduleScan'

        # start_time and end_time format used for converting datetime to and from format required for API
        time_format = '%Y%m%dT%H%M%S'
