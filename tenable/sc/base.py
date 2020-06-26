'''
Common Themes
=============

Tenable.sc CRUD within pyTenable
--------------------------------

pyTenable allows for the ability to leverage both the naturalized inputs as well
as passing the raw parameters within the same structure.  In some cases this
doesn't seem immediately obvious, however allows for the ability to pass
parameters that either haven't yet been, or in some cases, may never be
interpreted by the library.

For example, in the alerts API, you could pass the snake_cased
``always_exec_on_trigger`` or you could pass what the API endpoint itself
expects, which is ``executeOnEveryTrigger``.  The snake-cased version expects a
boolean value, which will be converted into the string value that camelCased
variant expects.  You'll see this behavior a lot throughout the library, and is
intended to allow you to sidestep most things should you need to.  For example,
in the alerts API again, you may not want to pass a trigger as
``trigger=('sumip', '>=', '100')`` and instead pass as the parameters that are
to be written into the JSON request:
``triggerName='sumip', triggerOperator='>=', triggerValue='100'``.  Both of
these methods will produce the same JSON request, and the the option is yours
to use the right way for the job.

Along these same lines, its possible to see how the JSON documents are being
constructed by simply looking at the ``_constructor`` methods for each
APIEndpoint class.  If pyTenable is getting in your way, you can almost always
sidestep it and pass the exact dictionary you wish to pass on to the API.

Schedule Dictionaries
---------------------

A dictionary detailing the repeating schedule within Tenable.sc.  This
dictionary consists of 1 or 3 parameters, depending on the type of schedule.
In all of the definitions except ``ical``, a  single parameter of ``type`` is
passed with lone of the following values: ``ical``, ``never``, ``rollover``, and
``template``.  If no document is specified, then the default of ``never`` is
assumed.  For repeating scans, you'll have to use the type of ``ical`` and also
specify the ``start`` and ``repeatRule`` parameters as well.  The ``start``
parameter is an
`iCal DateTime Form #3 <https://tools.ietf.org/html/rfc5545#section-3.3.5>`_
formatted string specifying the date and time in which to start the repeating
event.  The ``repeatRule`` parameter is an
`iCal Recurrance Rule <https://tools.ietf.org/html/rfc5545#section-3.3.10>`_
formatted string.

* Example Never Declaration:

.. code-block:: python

    {'type': 'never'}

* Example daily event starting at 9am Eastern

.. code-block:: python

    {
        'type': 'ical',
        'start': 'TZID=America/New_York:20190214T090000',
        'repeatRule': 'FREQ=DAILY;INTERVAL=1'
    }

* Example weekly event every Saturday at 8:30pm Eastern

.. code-block:: python

    {
        'type': 'ical',
        'start': 'TZID=America/New_York:20190214T203000',
        'repeatRule': 'FREQ=WEEKLY;BYDAY=SA;INTERVAL=1'
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
            :obj:`dict`:
                The dictionary structure of the expanded asset list combinations.
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

    def _query_constructor(self, *filters, **kw):
        '''
        Constructs an analysis query.  This part has been pulled out of the
        _analysis method and placed here so that it can be re-used in other
        part of the library.
        '''
        if 'filters' in kw:
            # if filters are explicitly called, then we will replace the
            # implicit filters with the explicit ones and remove the entry from
            # the keywords dictionary
            filters = self._check('filters', kw['filters'], list)
            del(kw['filters'])

        if 'query' not in kw and 'tool' in kw and 'type' in kw:
            kw['query'] = {
                'tool': kw['tool'],
                'type': kw['type'],
                'filters': list()
            }
            if 'query_id' in kw:
                # Request the specific query ID provided and fetch only the filters
                query_response = self._api.get(
                    'query/{}?fields=filters'.format(
                        kw['query_id'])).json()['response']

                # Extract the filters or set to null if nothing is returned
                query_filters = query_response.get('filters', list())

                kw['query']['filters'] = query_filters

            for f in filters:
                if kw['type'] == 'ticket':
                    item = {'filterName': f[0], 'value': f[1]}
                else:
                    item = {'filterName': f[0], 'operator': f[1]}

                if len(f) >= 3:
                    if (isinstance(f[2], tuple)
                      and f[1] == '~' and f[0] == 'asset'):
                        # if this is a asset combination, then we will want to
                        # expand the tuple into the expected dictionary
                        # structure that the API is expecting.
                        item['value'] = self._combo_expansion(f[2])
                    elif (isinstance(f[2], list)
                      and all(isinstance(i, int) for i in f[2])):
                        # if the value is a list and all of the items within
                        # that list are integers, then we can safely assume that
                        # this is a list of integer ids that need to be expanded
                        # into a list of dictionaries.
                        item['value'] = [dict(id=str(i)) for i in f[2]]
                    elif (isinstance(f[2], int) and f[0] in ['asset',]):
                        # If the value is an integer, then we will want to
                        # expand the value into a dictionary with an id attr.
                        item['value'] = dict(id=str(f[2]))
                    else:
                        # if we don't have any specific conditions set, then
                        # simply return the value parameter assigned to the
                        # "value" attribute
                        item['value'] = f[2]

                # Added this here to make the filter list overloadable.  As SC
                # only supports one filter of a given type, if an existing
                # filter is already in the list, we will overload it with the
                # new one.  This allows for the ability to overload query
                # filters if need be, or to overload a saved filterset that
                # someone is appending to.
                flist = [i['filterName'] for i in kw['query']['filters']]
                if f[0] in flist:
                    kw['query']['filters'].pop(flist.index(f[0]))

                # Add the newly expanded filter to the filters list as long as
                # both the operator and value are not None.  If both are none,
                # then skip appending.  This should allow for effectively
                # removing an unwanted filter from a query if a query id is
                # specified.
                if f[1] != None and f[2] != None:
                    kw['query']['filters'].append(item)
            del(kw['type'])
        return kw

    def _schedule_constructor(self, item):
        '''
        Handles creation of the schedule sub-document.
        '''
        self._check('schedule:item', item, dict)
        item['type'] = self._check('schedule:type',  item.get('type'), str,
            choices=['ical', 'dependent', 'never', 'rollover', 'template', 'now'],
            default='never')
        if item['type'] == 'ical':
            self._check('schedule:start', item.get('start'), str)
            self._check('schedule:repeatRule', item.get('repeatRule'), str)
        if item['type'] == 'dependent':
            self._check('schedule:dependentID', item.get('dependentID'), int)
        return item

class SCResultsIterator(APIResultsIterator):
    def _get_page(self):
        '''
        Retrieves the next page of results when the current page has been
        exhausted.
        '''
        # First we need to see if there is a page limit and if there is, have
        # we run into that limit.  If we have, then return a StopIteration
        # exception.
        if self._pages_total and self._pages_requested >= self._pages_total:
            raise StopIteration()

        # Now we need to do is construct the query with the current offset
        # and limits
        query = self._query
        query['startOffset'] = self._offset
        query['endOffset'] = self._limit + self._offset

        # Lets actually call the API for the data at this point.
        resp = self._api.get(self._resource, params=query).json()

        # Now that we have the response, lets reset any counters we need to,
        # and increment things like the page counter, offset, etc.
        self.page_count = 0
        self._pages_requested += 1
        self._offset += self._limit
        self._raw = resp
        self.page = resp['response']

        # As no total is returned via the API, we will simply need to re-compute
        # the total to be N+1 every page as long as the page of data is equal to
        # the limit.  If we ever get a page of data that is less than the limit,
        # then we will set the total to be the count + page length.
        if len(resp['response']) < self._limit:
            self.total = self.count + len(resp['response'])
        else:
            self.total = self.count + self._limit + 1