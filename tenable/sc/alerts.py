'''
alerts
======

The following methods allow for interaction into the Tenable.sc
`Alert <https://docs.tenable.com/sccv/api/Alert.html>`_ API.

Methods available on ``sc.alerts``:

.. rst-class:: hide-signature
.. autoclass:: AlertAPI

    .. automethod:: create
    .. automethod:: delete
    .. automethod:: details
    .. automethod:: edit
    .. automethod:: execute
    .. automethod:: list

.. _iCal Date-Time:
    https://tools.ietf.org/html/rfc5545#section-3.3.5
.. _iCal Recurrence Rule:
    https://tools.ietf.org/html/rfc5545#section-3.3.10
'''
from .base import SCEndpoint
from tenable.utils import dict_merge

class AlertAPI(SCEndpoint):
    def _constructor(self, *filters, **kw):
        '''
        Handles building an alert document.
        '''

        # call the analysis query constructor to assemble a query.
        if len(filters) > 0:
            # checking to see if data_type was passed.  If it wasn't then we
            # will set the value to the default of 'vuln'.
            if 'data_type' not in kw:
                kw['data_type'] = 'vuln'
            kw['type'] = kw['data_type']
            kw['tool'] = ''
            kw = self._query_constructor(*filters, **kw)
            del(kw['data_type'])
            del(kw['query']['tool'])
            del(kw['tool'])
        elif 'query_id' in kw:
            kw = self._query_constructor(*filters, **kw)

        if 'name' in kw:
            kw['name'] = self._check('name', kw['name'], str)

        if 'description' in kw:
            kw['description'] = self._check(
                'description', kw['description'], str)

        if 'query' in kw:
            kw['query'] = self._check('query', kw['query'], dict)

        if 'always_exec_on_trigger' in kw:
            # executeOnEveryTrigger expected a boolean response as a lower-case
            # string.  We will accept a boolean and then transform it into a
            # string value.
            kw['executeOnEveryTrigger'] = str(self._check(
                'always_exec_on_trigger', kw['always_exec_on_trigger'], bool)).lower()
            del(kw['always_exec_on_trigger'])

        if 'trigger' in kw:
            # here we will be expanding the trigger from the common format of
            # tuples that we are using within pytenable into the native
            # supported format that SecurityCenter expects.
            self._check('trigger', kw['trigger'], tuple)
            kw['triggerName'] = self._check(
                'triggerName', kw['trigger'][0], str)
            kw['triggerOperator'] = self._check(
                'triggerOperator', kw['trigger'][1], str,
                choices=['>=', '<=', '=', '!='])
            kw['triggerValue'] = self._check(
                'triggerValue', kw['trigger'][2], str)
            del(kw['trigger'])

        # hand off the building the schedule sub-document to the schedule
        # document builder.
        if 'schedule' in kw:
            kw['schedule'] = self._schedule_constructor(kw['schedule'])

        # FR: at some point we should start looking into checking and
        #     normalizing the action document.
        return kw

    def list(self, fields=None):
        '''
        Retrieves the list of alerts.

        :sc-api:`alert: list <Alert.html#AlertRESTReference-/alert>`

        Args:
            fields (list, optional):
                A list of attributes to return for each alert.

        Returns:
            :obj:`dict`:
                A list of alert resources.

        Examples:
            >>> for alert in sc.alerts.list()['manageable']:
            ...     pprint(alert)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str)
                for f in fields])

        return self._api.get('alert', params=params).json()['response']

    def details(self, id, fields=None):
        '''
        Returns the details for a specific alert.

        :sc-api:`alert: details <Alert.html#AlertRESTReference-/alert/{id}>`

        Args:
            id (int): The identifier for the alert.
            fields (list, optional): A list of attributes to return.

        Returns:
            :obj:`dict`:
                The alert resource record.

        Examples:
            >>> alert = sc.alerts.detail(1)
            >>> pprint(alert)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) for f in fields])

        return self._api.get('alert/{}'.format(self._check('id', id, int)),
            params=params).json()['response']

    def create(self, *filters, **kw):
        '''
        Creates a new alert.  The fields below are explicitly checked, however
        any additional parameters mentioned in the API docs can be passed to the
        document constructor.

        :sc-api:'alert: create <Alert.html#alert_POST>`

        Args:
            *filters (tuple):
                A filter expression.  Refer to the detailed description within
                the analysis endpoint documentation for more details on how to
                formulate filter expressions.
            data_type (str):
                The type of filters being used.  Must be of type ``lce``,
                ``ticket``, ``user``, or ``vuln``.  If no data-type is
                specified, then the default of ``vuln`` will be set.
            name (str): The name of the alert.
            description (str, optional): A description for the alert.
            trigger (tuple):
                A tuple in the filter-tuple format detailing what would
                constitute a trigger.  For example: ``('sumip', '=', '1000')``.
            always_exec_on_trigger (bool, optional):
                Should the trigger always execute when the trigger fires, or
                only execute when the returned data changes?
                Default is ``False``.
            schedule (dict, optional):
                This is the schedule dictionary that will inform Tenable.sc how
                often to run the alert.  If left unspecified then we will
                default to ``{'type': 'never'}``.  For more information refer to
                `Schedule Dictionaries`_
            action (list):
                The action(s) that will be performed when the alert trigger
                fires.  Each action is a dictionary detailing what type of
                action to take, and the details surrounding that action.  The
                supported type of actions are ``email``, ``notifications``,
                ``report``, ``scan``, ``syslog``, and ``ticket``.  The following
                examples lay out each type of action as an example:

                * Email action type:

                .. code-block:: python

                    {'type': 'email',
                     'subject': 'Example Email Subject',
                     'message': 'Example Email Body'
                     'addresses': 'user1@company.com\\nuser2@company.com',
                     'users': [{'id': 1}, {'id': 2}],
                     'includeResults': 'true'}

                * Notification action type:

                .. code-block:: python

                    {'type': 'notification',
                     'message': 'Example notification',
                     'users': [{'id': 1}, {'id': 2}]}

                * Report action type:

                .. code-block:: python

                    {'type': 'report',
                     'report': {'id': 1}}

                * Scan action type:

                .. code-block:: python

                    {'type': 'scan',
                     'scan': {'id': 1}}

                * Syslog action type:

                .. code-block:: python

                    {'type': 'syslog',
                     'host': '127.0.0.1',
                     'port': '514',
                     'message': 'Example Syslog Message',
                     'severity': 'Critical'}

                * Ticket action type:

                .. code-block:: python

                    {'type': 'ticket',
                     'assignee': {'id': 1},
                     'name': 'Example Ticket Name',
                     'description': 'Example Ticket Description',
                     'notes': 'Example Ticket Notes'}

        Returns:
            :obj:`dict`:
                The alert resource created.

        Examples:
            >>> sc.alerts.create(
            ...     ('severity', '=', '3,4'),
            ...     ('exploitAvailable', '=', 'true'),
            ...     trigger=('sumip', '>=', '100'),
            ...     name='Too many High or Critical and Exploitable',
            ...     action=[{
            ...         'type': 'notification',
            ...         'message': 'Too many High or Crit Exploitable Vulns',
            ...         'users': [{'id': 1}]
            ...     }])
        '''
        payload = self._constructor(*filters, **kw)
        return self._api.post('alert', json=payload).json()['response']

    def edit(self, id, *filters, **kw):
        '''
        Updates an existing alert.  All fields are optional and will overwrite
        the existing value.

        :sc-api:`alert: update <Alert.html#alert_id_PATCH>`

        Args:
            if (int): The alert identifier.
            *filters (tuple):
                A filter expression.  Refer to the detailed description within
                the analysis endpoint documentation for more details on how to
                formulate filter expressions.
            data_type (str):
                The type of filters being used.  Must be of type ``lce``,
                ``ticket``, ``user``, or ``vuln``.  If no data-type is
                specified, then the default of ``vuln`` will be set.
            name (str, optional): The name of the alert.
            description (str, optional): A description for the alert.
            trigger (tuple, optional):
                A tuple in the filter-tuple format detailing what would
                constitute a trigger.  For example: ``('sumip', '=', '1000')``.
            always_exec_on_trigger (bool, optional):
                Should the trigger always execute when the trigger fires, or
                only execute when the returned data changes?
                Default is ``False``.
            schedule (dict, optional):
                This is the schedule dictionary that will inform Tenable.sc how
                often to run the alert.  If left unspecified then we will
                default to ``{'type': 'never'}``.  For more information refer to
                `Schedule Dictionaries`_
            action (list):
                The action(s) that will be performed when the alert trigger
                fires.  Each action is a dictionary detailing what type of
                action to take, and the details surrounding that action.

        Returns:
            :obj:`dict`:
                The modified alert resource.

        Examples:
            >>> sc.alerts.update(1, name='New Alert Name')
        '''
        payload = self._constructor(*filters, **kw)
        return self._api.patch('alert/{}'.format(
            self._check('id', id, int)), json=payload).json()['response']

    def delete(self, id):
        '''
        Deletes the specified alert.

        :sc-api:`alert: delete <Alert.html#alert_id_DELETE>`

        Args:
            id (int): The alert identifier.

        Returns:
            :obj:`str`:
                The response code of the action.

        Examples:
            >>> sc.alerts.delete(1)
        '''
        return self._api.delete('alert/{}'.format(
            self._check('id', id, int))).json()['response']

    def execute(self, id):
        '''
        Executes the specified alert.

        :sc-api:`alert: execute <Alert.html#AlertRESTReference-/alert/{id}/execute>`

        Args:
            id (int): The alert identifier.

        Returns:
            :obj:`dict`:
                The alert resource.
        '''
        return self._api.post('alert/{}/execute'.format(
            self._check('id', id, int))).json()['response']
