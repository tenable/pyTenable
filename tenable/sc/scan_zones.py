'''
scan_zones
==========

The following methods allow for interaction into the Tenable.sc 
`Scan Zone <https://docs.tenable.com/sccv/api/Scan-Zone.html>`_ API.  These 
items are typically seen under the **Scan Zones** section of Tenable.sc.

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

        + `scan-zone: create <https://docs.tenable.com/sccv/api/Scan-Zone.html#zone_POST>`_

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
            dict: The newly created scan zone. 
        
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

        + `scan-zone: details <https://docs.tenable.com/sccv/api/Scan-Zone.html#zone_id_GET>`_

        Args:
            id (int): The identifier for the scan.
            fields (list, optional): A list of attributes to return.

        Returns:
            dict: The scan zone resource record.

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

        + `scan-zone: edit <https://docs.tenable.com/sccv/api/Scan-Zone.html#zone_id_PATCH>`_

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
            dict: The newly updated scan zone. 
        
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

        + `scan-zone: list <https://docs.tenable.com/sccv/api/Scan-Zone.html#zone_GET>`_

        Args:
            fields (list, optional): 
                A list of attributes to return for each scan.

        Returns:
            list: A list of scan zone resources.

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

        + `scan-zone: delete <https://docs.tenable.com/sccv/api/Scan-Zone.html#zone_id_DELETE>`_

        Args:
            id (int): The numeric identifier for the scan-zone to remove.
        
        Returns:
            str: An empty response.
        
        Examples:
            >>> sc.scan_zones.delete(1)
        '''
        return self._api.delete('zone/{}'.format(
            self._check('id', id, int))).json()['response']