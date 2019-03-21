# -*- coding: utf-8 -*-
"""
"""
from tenable.sc.base import SCEndpoint



class OrganizationAPI(SCEndpoint):

    def _constructor(self, **kw):
        '''
        Organization document constructor
        '''
        if 'name' in kw:
            kw["name"] = self._check('name', kw['name'], str)

        if 'description' in kw:
            kw['description'] = self._check('description', kw.get('description', ''), str)

        if 'address' in kw:
            kw['address'] = self._check('address', kw.get('address', ''), str)

        if 'city' in kw:
            kw['city'] = self._check('city', kw.get('city', ''), str)

        if 'state' in kw:
            kw['state'] = self._check('state', kw.get('state', ''), str)

        if 'country' in kw:
            kw['country'] = self._check('country', kw.get('country'), str)

        if 'phone' in kw:
            kw['phone'] = self._check('phone', kw.get('phone'), str)

        if 'lces' in kw:
            kw["lces"] = self._check('lces', kw['lces'], list, default=[])

        if 'zone_selection' in kw:
            kw["zoneSelection"] = self._check(
                'zone_selection', kw['zone_selection'], str,
                choices=["auto_only", "locked", "selectable",
                         "selectable+auto", "selectable+auto_restricted"])
            del kw['zone_selection']

        if 'restricted_ips' in kw:
            kw['restrictedIPs'] = self._check(
                'restrictedIPs', kw['restricted_ips'], str)
            del kw['restricted_ips']

        if 'repo' in kw:
            kw["repositories"] = [{'id': int(r.get('id'))} for r in self._check(
                'repo', kw['repo'], list, default=[]) if r.get('id')]
            del kw['repo']

        if 'pub_sites' in kw:
            kw["pubSites"] = [{'id': int(p.get('id'))} for p in self._check(
                'pub_sites', kw['pub_sites'], list, default=[]
            ) if p.get('id')]
            del kw["pub_sites"]

        if 'ldaps' in kw:
            kw["ldaps"] = [{'id': int(p.get('id'))} for p in self._check(
                'ldaps', kw['ldaps'], list, default=[]
            ) if p.get('id')]

        if 'nessus_managers' in kw:
            kw["nessusManagers"] = [{'id': int(n.get('id'))} for n in self._check(
                'nessus_managers', kw['nessus_managers'], list, default=[]
            ) if n.get('id')]
            del kw['nessus_managers']

        if 'ip_info_links' in kw:
            kw['ipInfoLinks'] = [{
                'link': i.get('link'),
                'name': i.get('name')
            } for i in self._check(
                'ip_info_links', kw['ip_info_links'], list, default=[]
            ) if i.get('link')]
            del kw['ip_info_links']

        if 'vuln_score_low' in kw:
            kw['vulnScoreLow'] = self._check(
                'vuln_score_low', kw['vuln_score_low'], int, default=1)
            del kw['vuln_score_low']

        if 'vuln_score_medium' in kw:
            kw['vulnScoreMedium'] = self._check(
                'vuln_score_medium', kw['vuln_score_medium'], int, default=3)
            del kw['vuln_score_medium']

        if 'vuln_score_high' in kw:
            kw['vulnScoreHigh'] = self._check(
                'vuln_score_high', kw['vuln_score_high'], int, default=10)
            del kw['vuln_score_high']

        if 'vuln_score_critical' in kw:
            kw['vulnScoreCritical'] = self._check(
                'vuln_score_critical', kw['vuln_score_critical'], int, default=40)
            del kw['vuln_score_critical']

        return kw

    def create(self, **kw):
        kw = self._constructor(**kw)
        return self._api.post('organization', json=kw).json()['response']

    def list(self, fields=None):
        '''
        Retrieves a list of organizations.

        + `SC organization List <https://docs.tenable.com/sccv/api/Organization.html#OrganizationRESTReference-/organization>`_

        Args:
            fields (list, optional):
                The list of fields that are desired to be returned.  For details
                on what fields are available, please refer to the details on the
                request within the organization list API doc.
            repo_type (str, optional):
                Restrict the response to a specific type of organization.  If not
                set, then all organization types will be returned.  Allowed types
                are ``All``, ``Local``, ``Remote``, and ``Offline``.

        Returns:
            list: List of organization definitions.

        Examples:
            Retrieve all of all of the organizations:

            >>> repos = sc.organizations.list()

            Retrieve all of the remote organizations:

            >>> repos = sc.organizations.list(repo_type='Remote')
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str)
                                         for f in fields])
        return self._api.get('organization', params=params).json()['response']

    def details(self, id, fields=None):
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) for f in fields])

        return self._api.get('organization/{}'.format(
            self._check('id', id, int)), params=params).json()['response']

    def edit(self, org_id, **kw):
        '''Updates an existing organization

        Edits the Organization associated with {id}, changing only the passed in fields.

        + `SC Organization Edit <https://docs.tenable.com/sccv/api/Organization.html#organization_id_PATCH>`_

        Examples:
            >>> sc.organization.edit(1, name='New Name')
        '''
        kw = self._constructor(**kw)
        return self._api.patch('organization/{}'.format(
            self._check('id', org_id, int)), json=kw).json()['response']

    def delete(self, org_id):
        '''
        Remove the specified organization from Tenable.sc

        + `SC organization Delete <https://docs.tenable.com/sccv/api/Organization.html#organization_id_DELETE>`_

        Args:
            id (int): The numeric id of the organization to delete.

        Returns:
            str: Empty response string

        Examples:
            >>> sc.organization.delete(1)
        '''
        return self._api.delete('organization/{}'.format(
            self._check('id', org_id, int))).json()['response']
