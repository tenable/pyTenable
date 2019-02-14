'''
Common Components and Themes for Tenable.sc
===========================================

Schedule Dictionaries
---------------------

A dictionary detailing the repeating schedule within Tenable.sc.  This 
dictionary consists of 1 or 3 parameters, depending on the type of schedule.  
In all of the definitions except ``ical``, a  single parameter of ``type`` is 
passed with lone of the following values: ``ical``, ``never``, ``rollover``, and
``template``.  If no document is specified, then the default of ``never`` is 
assumed.  For repeating scans, you'll have to use the type of ``ical`` and also 
specify the ``start`` and ``rrule`` parameters as well.  The ``start`` parameter 
is an `iCal DateTime Form #3 <https://tools.ietf.org/html/rfc5545#section-3.3.5>`_
formatted string specifying the date and time in which to start the repeating 
event.  The ``rrule`` parameter is an 
`iCal Recurrance Rule <https://tools.ietf.org/html/rfc5545#section-3.3.10>`_
formatted string.

* Example Never Declaration:

.. code-block:: python

    {'type': 'never'}

* Example daily event starting at 9am Eastern

.. code-block:: python

    {
        'type': 'ical',
        'start': 'TZID=America/New York:20190214T090000',
        'rrule': 'FREQ=DAILY;INTERVAL=1'
    }

* Example weekly event every Saturday at 8:30pm Eastern

.. code-block:: python

    {
        'type': 'ical',
        'start': 'TZID=America/New York:20190214T203000',
        'rrule': 'FREQ=WEEKLY;BYDAY=SA;INTERVAL=1'
    }

There are detailed instructions in the RFC documentation on how to construct
these recurrence rules.  Further there are some packages out there to aid in 
converting more human-readable text into recurrence rules, such as the 
`recurrent package <https://pypi.org/project/recurrent/>`_ for example.
'''
from tenable.base import APIEndpoint, APIResultsIterator

class SCEndpoint(APIEndpoint):
    def _combo_expansion(self, item):
        '''
        Expands the asset combination expressions from nested tuples to the
        nested dictionary structure that's expected.

        Args:
            item
        
        Returns:
            dict: The dictionary structure of the expanded asset list combinations.
        '''

        # the operator conversion dictionary.  The UI uses "and", "or", and
        # "not" whereas the API uses "intersection", "union", and "compliment".
        # if the user is passing us the tuples, lets assume that they are using
        # the UI definitions and not the API ones.
        oper = {
            'and': 'intersection',
            'or': 'union',
            'not': 'complement'
        }

        # some simple checking to ensure that we are being passed good data
        # before we expand the tuple.
        if len(item) < 2 or len(item) > 3:
            raise TypeError('{} must be exactly 1 operator and 1-2 items'.format(item))
        self._check('operator', item[0], str, choices=oper.keys())
        self._check('operand1', item[1], [int, tuple])
        if len(item) == 3:
            self._check('operand2', item[2], [int, tuple])

        resp = {'operator': oper[item[0].lower()]}

        # we need to expand the operand.  If the item is a nested tuple, then
        # we will call ourselves and pass the tuple.  If not, then we will
        # simply return a dictionary with the id value set to the integer that
        # was passed.
        if isinstance(item[1], tuple):
            resp['operand1'] = self._combo_expansion(item[1])
        else:
            resp['operand1'] = {'id': str(item[1])}

        # if there are 2 operators in the tuple, then we will want to expand the
        # second one as well. If the item is a nested tuple, then we will call 
        # ourselves and pass the tuple.  If not, then we will simply return a 
        # dictionary with the id value set to the integer that was passed.
        if len(item) == 3:
            if isinstance(item[2], tuple):
                resp['operand2'] = self._combo_expansion(item[2])
            else:
                resp['operand2'] = {'id': str(item[2])}

        # return the response to the caller.
        return resp
    def _schedule_constructor(self, item):
        '''
        Handles creation of the schedule sub-document.
        '''
        resp = {'type': self._check('schedule:type', item['type'], str, 
            choices=['ical', 'dependent', 'never', 'rollover', 'template'],
            default='never')}
        
        if resp['type'] == 'ical' and 'start' in item and 'repeatRule' in item:
            resp['start'] = self._check('schedule:start', item['start'], str)
            resp['repeatRule'] = self._check(
                'schedule:repeatRule', item['repeatRule'], str)
        return resp

class SCResultsIterator(APIResultsIterator):
    pass
