'''
scan_zones
==========

The following methods allow for interaction into the Tenable.sc
:sc-api:`Scan Zone <Scan-Zone.html>` API.  These items are typically seen under
the **Scan Zones** section of Tenable.sc.

Methods available on ``sc.scan_zones``:

.. rst-class:: hide-signature
.. autoclass:: ScanZoneAPI

    .. automethod:: create
    .. automethod:: delete
    .. automethod:: details
    .. automethod:: edit
    .. automethod:: list
'''
from .base import SCEndpoint

class ScanZoneAPI(SCEndpoint):
    def _constructor(self, **kw):
        '''
        Handles parsing the keywords and returns a scan zone definition document
        '''
        if 'name' in kw:
            # Validate that the name is a string
            self._check('name', kw['name'], str)

        if 'description' in kw:
            # validate that the description is a string.
            self._check('description', kw['description'], str)

        if 'ips' in kw:
            # convert the ips list into the comma-seperated list of ips that
            # the API expects to receive.
            kw['ipList'] = ','.join([self._check('ip', i, str)
                for i in self._check('ips', kw['ips'], list)])
            del(kw['ips'])

        if 'scanner_ids' in kw:
            # convert the list of scanner ids into a list of documents
            # containing the scanner id.
            kw['scanners'] = [{'id': self._check('id', i, int)}
                for i in self._check('scanner_ids', kw['scanner_ids'], list)]
            del(kw['scanner_ids'])

        return kw

    def create(self, name, **kw):
        '''
        Creates a scan zone.

        :sc-api:`scan-zone: create <Scan-Zone.html#zone_POST>`

        Args:
            name (str): The name of the scan zone
            description (str, optional):
                A description for the scan zone.
            ips (list, optional):
                The list of IP addresses, CIDRs, or IP ranges that encompass the
                scan zone.
            scanner_ids (list, optional):
                A list of scanner ids to associate to the scan zone.

        Returns:
            :obj:`dict`:
                The newly created scan zone.

        Examples:
            >>> zone = sc.scan_zones.create('Example Scan Zone',
            ...     ips=['127.0.0.1'], scanner_ids=[1])
        '''
        kw['name'] = name
        payload = self._constructor(**kw)
        return self._api.post('zone', json=payload).json()['response']

    def details(self, id, fields=None):
        '''
        Returns the details for a specific scan zone.

        :sc-api:`scan-zone: details <Scan-Zone.html#zone_id_GET>`

        Args:
            id (int): The identifier for the scan.
            fields (list, optional): A list of attributes to return.

        Returns:
            :obj:`dict`:
                The scan zone resource record.

        Examples:
            >>> zone = sc.scan_zones.details(1)
            >>> pprint(zone)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) for f in fields])

        return self._api.get('zone/{}'.format(self._check('id', id, int)),
            params=params).json()['response']

    def edit(self, id, **kw):
        '''
        Edits a scan zone.

        :sc-api:`scan-zone: edit <Scan-Zone.html#zone_id_PATCH>`

        Args:
            description (str, optional):
                A description for the scan zone.
            ips (list, optional):
                The list of IP addresses, CIDRs, or IP ranges that encompass the
                scan zone.
            name (str, optional): The name of the scan zone
            scanner_ids (list, optional):
                A list of scanner ids to associate to the scan zone.

        Returns:
            :obj:`dict`:
                The newly updated scan zone.

        Examples:
            >>> zone = sc.scan_zones.create(1,
            ...     ips=['127.0.0.1'], scanner_ids=[1])
        '''
        payload = self._constructor(**kw)
        return self._api.patch('zone/{}'.format(self._check('id', id, int)),
            json=payload).json()['response']


    def list(self, fields=None):
        '''
        Retrieves the list of scan zone definitions.

        :sc-api:`scan-zone: list <Scan-Zone.html#zone_GET>`

        Args:
            fields (list, optional):
                A list of attributes to return for each scan.

        Returns:
            :obj:`list`:
                A list of scan zone resources.

        Examples:
            >>> for zone in sc.scan_zones.list():
            ...     pprint(zone)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str)
                for f in fields])

        return self._api.get('zone', params=params).json()['response']

    def delete(self, id):
        '''
        Removes the specified scan zone.

        :sc-api:`scan-zone: delete <Scan-Zone.html#zone_id_DELETE>`

        Args:
            id (int): The numeric identifier for the scan-zone to remove.

        Returns:
            :obj:`str`:
                An empty response.

        Examples:
            >>> sc.scan_zones.delete(1)
        '''
        return self._api.delete('zone/{}'.format(
            self._check('id', id, int))).json()['response']