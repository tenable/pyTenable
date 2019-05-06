'''
groups
======

The following methods allow for interaction into the Tenable.sc 
`Group <https://docs.tenable.com/sccv/api/Group.html>`_ API.  These 
items are typically seen under the **User Groups** section of Tenable.sc.

Methods available on ``sc.groups``:

.. rst-class:: hide-signature
.. autoclass:: GroupAPI

    .. automethod:: create
    .. automethod:: delete
    .. automethod:: details
    .. automethod:: edit
    .. automethod:: list
'''
from .base import SCEndpoint

class GroupAPI(SCEndpoint):
    def _constructor(self, **kw):
        '''
        Handles parsing the keywords and returns a group definition document
        '''
        if 'name' in kw:
            self._check('name', kw['name'], str)
        
        if 'description' in kw:
            self._check('description', kw['description'], str)
        
        mapping = {
            'viewable': 'definingAssets',
            'repos': 'repositories',
            'lce_ids': 'lces',
            'asset_lists': 'assets',
            'scan_policies': 'policies',
            'query_ids': 'queries',
            'scan_creds': 'credentials',
            'dashboards': 'dashboardTabs',
            'report_cards': 'arcs',
            'audit_files': 'auditFiles'
        }
        for k, v in mapping.items():
            if k in kw:
                # For each item in the mapping, expand the kwarg if it exists
                # into a list of dictionaries with an id attribute.  Associate
                # the expanded list to the value of the hash table and delete
                # the original kwarg.
                kw[v] = [{'id': self._check('{}:item'.format(k), i, int)}
                    for i in self._check(k, kw[k], list)]
                del(kw[k])
        return kw
    
    def create(self, name, **kw):
        '''
        Creates a group.

        + `group: create <https://docs.tenable.com/sccv/api/Group.html#group_POST>`_

        Args:
            name (str): The name of the user group
            asset_lists (list, optional): 
                List of asset list ids to allow this group to access.
            audit_files (list, optional):
                List of audit file ids to allow this group to access.
            dashboards (list, optional):
                List of dashboard ids to allow this group to access.
            lce_ids (list, optional):
                List of LCE ionstance ids to allow this group to access.
            query_ids (list, optional):
                List of query ids to allow this group to access.
            report_cards (list, optional):
                List of report card ids to allow this group to access.
            repos (list, optional):
                List of repository ids to allow this group to access.
            scan_creds (list, optional):
                List of scanning credential ids to allow this group to access.
            scan_policies (list, optional):
                List of scan policy ids to allow this group to access.
            viewable (list, optional):
                List of asset list ids to use for the purposes of restricting
                what members of this group can see within Tenable.sc.
        
        Returns:
            dict: The newly created group. 
        
        Examples:
            >>> group = sc.groups.create('New Group')
        '''
        kw['name'] = name
        payload = self._constructor(**kw)
        return self._api.post('group', json=payload).json()['response']
    
    def details(self, id, fields=None):
        '''
        Returns the details for a specific group.

        + `group: details <https://docs.tenable.com/sccv/api/Group.html#GroupRESTReference-/group/{id}>`_

        Args:
            id (int): The identifier for the group.
            fields (list, optional): A list of attributes to return.

        Returns:
            dict: The group resource record.

        Examples:
            >>> group = sc.groups.details(1)
            >>> pprint(group)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) for f in fields])

        return self._api.get('group/{}'.format(self._check('id', id, int)),
            params=params).json()['response']
    
    def edit(self, id, **kw):
        '''
        Edits a group.

        + `group: edit <https://docs.tenable.com/sccv/api/Group.html#group_id_PATCH>`_

        Args:
            asset_lists (list, optional): 
                List of asset list ids to allow this group to access.
            audit_files (list, optional):
                List of audit file ids to allow this group to access.
            dashboards (list, optional):
                List of dashboard ids to allow this group to access.
            lce_ids (list, optional):
                List of LCE ionstance ids to allow this group to access.
            name (str, optional): 
                The name of the user group
            query_ids (list, optional):
                List of query ids to allow this group to access.
            report_cards (list, optional):
                List of report card ids to allow this group to access.
            repos (list, optional):
                List of repository ids to allow this group to access.
            scan_creds (list, optional):
                List of scanning credential ids to allow this group to access.
            scan_policies (list, optional):
                List of scan policy ids to allow this group to access.
            viewable (list, optional):
                List of asset list ids to use for the purposes of restricting
                what members of this group can see within Tenable.sc.
        
        Returns:
            dict: The newly updated group. 
        
        Examples:
            >>> group = sc.groups.edit()
        '''
        payload = self._constructor(**kw)
        return self._api.patch('group/{}'.format(
            self._check('id', id, int)), json=payload).json()['response']

    def delete(self, id):
        '''
        Removes a group.

        + `group: delete <https://docs.tenable.com/sccv/api/Group.html#group_id_DELETE>`_

        Args:
            id (int): The numeric identifier for the group to remove.
        
        Returns:
            str: An empty response.
        
        Examples:
            >>> sc.groups.delete(1)
        '''
        return self._api.delete('group/{}'.format(
            self._check('id', id, int))).json()['response']
    
    def list(self, fields=None):
        '''
        Retrieves the list of scan zone definitions.

        + `group: list <https://docs.tenable.com/sccv/api/Group.html#group_GET>`_

        Args:
            fields (list, optional): 
                A list of attributes to return for each group.

        Returns:
            list: A list of group resources.

        Examples:
            >>> for group in sc.groups.list():
            ...     pprint(group)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) 
                for f in fields])
        
        return self._api.get('group', params=params).json()['response']
