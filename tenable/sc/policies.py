'''
policies
========

The following methods allow for interaction into the Tenable.sc 
`Scan Policies <https://docs.tenable.com/sccv/api/Scan-Policy.html>`_ API.  
These items are typically seen under the **Scan Policies** section of Tenable.sc.

Methods available on ``sc.policies``:

.. rst-class:: hide-signature
.. autoclass:: ScanPolicyAPI

    .. automethod:: copy
    .. automethod:: delete
    .. automethod:: details
    .. automethod:: export_policy
    .. automethod:: import_policy
    .. automethod:: list
    .. automethod:: share
    .. automethod:: template_details
    .. automethod:: template_list
'''
from .base import SCEndpoint
from tenable.errors import UnexpectedValueError
from tenable.utils import dict_merge, policy_settings
from io import BytesIO
import json

class ScanPolicyAPI(SCEndpoint):
    def _constructor(self, **kw):
        '''
        Document constructor for scan policies.
        '''
        if 'name' in kw:
            # Verify that the name attribute is a string.
            self._check('name', kw['name'], str)

        if 'context' in kw:
            # Verify the context if supplied.
            self._check('context', kw['context'], str, choices=['scan', ''])
        
        if 'description' in kw:
            # Verify that the description is a string
            self._check('description', kw['description'], str)
        
        if 'tags' in kw:
            # Verify that the tags keyword is a string.
            self._check('tags', kw['tags'], str)
        
        if 'preferences' in kw:
            # Validate that all of the preferences are K:V pairs of strings.
            for key in self._check('preferences', kw['preferences'], dict):
                self._check('preference:{}'.format(key), key, str)
                self._check('preference:{}:value'.format(key), 
                    kw['preferences'][key], str)
        
        if 'audit_files' in kw:
            # unflatten the audit_files list into a list of dictionaries.
            kw['auditFiles'] = [{'id': self._check('auditfile_id', a, int)} 
                for a in self._check('audit_files', kw['audit_files'], list)]
            del(kw['audit_files'])
        
        if 'template_id' in kw:
            # convert the policy template id into the appropriate sub-document.
            kw['policyTemplate'] = {
                'id': self._check('template_id', kw['template_id'], int)
            }
            del(kw['template_id'])
        
        if 'profile_name' in kw:
            # convert the snake-cased "profile_name" into the CamelCase
            # policyProfileName.
            kw['policyProfileName'] = self._check(
                'profile_name', kw['profile_name'], str)
            del(kw['profile_name'])
        
        if 'xccdf' in kw:
            # convert the boolean xccdf flag into the string equivalent of
            # generateXCCDFResults.
            kw['generateXCCDFResults'] = str(self._check(
                'xccdf', kw['xccdf'], bool)).lower()
            del(kw['xccdf'])
        
        if 'owner_id' in kw:
            # Convert the owner integer id into CamelCase equiv.
            kw['ownerID'] = self._check('owner_id', kw['owner_id'], int)
            del(kw['owner_id'])
        return kw
    
    def template_list(self, fields=None):
        '''
        Retrieved the list of scan policy templates.

        + `SC Scan Policy Template List <https://docs.tenable.com/sccv/api/Scan-Policy.html#policy_GET>`_

        Args:
            fields (list, optional): 
                The list of fields that are desired to be returned.  For details
                on what fields are available, please refer to the details on the
                request within the policy template list API doc.
        
        Returns:
            list: List of available policy templates
        
        Examples:
            >>> templates = sc.policies.template_list()
            >>> for policy in templates:
            ...     pprint(policy)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) 
                for f in fields])

        return self._api.get('policyTemplate', params=params).json()['response']
    
    def template_details(self, id, fields=None, remove_editor=True):
        '''
        Retrieves the details for a specified policy template.

        + `SC Scan Policy Template Details <https://docs.tenable.com/sccv/api/Scan-Policy-Templates.html#policyTemplate_id_GET>`_

        Args:
            id (int): The unique identifier for the policy template
            fields (list, optional): 
                The list of fields that are desired to be returned.  For details
                on what fields are available, please refer to the details on the
                request within the policy template details API doc.
            remove_editor (bol, optional):
                Should the response have the raw editor string removed?  The
                default is yes.
        
        Returns:
            dict: Details about the scan policy template
        
        Examples:
            >>> template = sc.policies.template_details(2)
            >>> pprint(template)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) 
                for f in self._check('fields', fields, list)])

        resp = self._api.get('policyTemplate/{}'.format(self._check('id', id, int)),
            params=params).json()['response']
        
        if 'editor' in resp:
            # Everything is packed JSON, so lets decode the JSON documents into 
            editor = json.loads(resp['editor'])

            # Now to decompose the embeddable credentials settings.  What we
            # intend to do here is return the default settings for every
            # credential set that can be returned.
            resp['credentials'] = dict()
            if 'credentials' in editor:
                emcreds = json.loads(editor['credentials'])
                for group in emcreds['groups']:
                    for item in group['credentials']:
                        resp['credentials'][item['id']] = policy_settings(item)
            
            # Now to perform the same action as we did for the credentials with
            # the policy preferences as well.
            resp['preferences'] = dict()
            for section in editor['sections']:
                if section['id'] != 'setup':
                    resp['preferences'] = dict_merge(resp['preferences'],
                        policy_settings(section))
            if remove_editor:
                del(resp['editor'])
        return resp
    
    def list(self, fields=None):
        '''
        Retrieved the list of Scan policies configured.

        + `SC Scan Policy List <https://docs.tenable.com/sccv/api/Scan-Policy.html#policy_GET>`_

        Args:
            fields (list, optional): 
                The list of fields that are desired to be returned.  For details
                on what fields are available, please refer to the details on the
                request within the policy list API doc.
        
        Returns:
            dict: usable & manageable scan policies.
        
        Examples:
            >>> policies = sc.policies.list()
            >>> for policy in policies['manageable']:
            ...     pprint(policy)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) 
                for f in self._check('fields', fields, list)])

        return self._api.get('policy', params=params).json()['response']

    def details(self, id, fields=None):
        '''
        Retrieves the details for a specified policy.

        + `SC Scan Policy Details <https://docs.tenable.com/sccv/api/Scan-Policy.html#policy_id_GET>`_

        Args:
            id (int): The unique identifier for the policy
            fields (list, optional): 
                The list of fields that are desired to be returned.  For details
                on what fields are available, please refer to the details on the
                request within the policy details API doc.
        
        Returns:
            dict: Details about the scan policy template
        
        Examples:
            >>> policy = sc.policies.details(2)
            >>> pprint(policy)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) 
                for f in self._check('fields', fields, list)])

        return self._api.get('policy/{}'.format(self._check('id', id, int)),
            params=params).json()['response']
    
    def create(self, **kw):
        '''
        Creates a new scan policy

        + `SC Scan Policy Create <https://docs.tenable.com/sccv/api/Scan-Policy.html#policy_POST>`_

        Args:
            name (str): The Name of the new scan policy
            audit_files (list, optional):
                A list of audit files (by integer id) to be used for the 
                scan policy.
            description (str, optional):
                An optional description for the policy
            preferences (dict, optional):
                A dictionary of settings that override the defaults within a
                policy template.
            profile_name (str, optional):
                The profile of the scan.  Default is an empty string.
            owner_id (int, optional):
                Define who shall own the policy by that user's integer identifer
            tags (str, optional):
                An optional tag identifier for the policy
            template_id (int, optional): 
                The identifier of the policy template to use.  If none is
                specified, the default id for the "Advanced Policy" will be
                used.
            xccdf (bool, optional):
                Should XCCDF results be generated?  The default is False.
            
        Returns:
            dict: The created scan policy resource.
        
        Examples:
            An example advanced policy with all of the default preferences.

            >>> sc.policies.create(
            ...     name='Example Advanced Policy')

            An example policy where we want to modify 
        '''
        # Firstly we need to check that some specific values are set
        if 'name' not in kw:
            raise UnexpectedValueError('name is a required parameter')
        kw['template_id'] = self._check(
            'template_id', kw.get('template_id', 1), int)

        # Next we will pull the template details and then pull out the default
        # settings for the template.
        template = self.template_details(kw['template_id'])
        
        # Next, if there are any preferences that the user provided, we will
        # overlay those on top of the now constructed defaults.
        kw['preferences'] = dict_merge(template['preferences'], 
            kw.get('preferences', dict()))
        
        policy = self._constructor(**kw)
        return self._api.post('policy', json=policy).json()['response']
    
    def edit(self, id, **kw):
        '''
        Edits an existing scan policy

        + `SC Scan Policy Edit <https://docs.tenable.com/sccv/api/Scan-Policy.html#policy_id_PATCH>`_

        Args:
            id (int): The unique identifier to the scan policy to edit
            audit_files (list, optional):
                A list of audit files (by integer id) to be used for the 
                scan policy.
            description (str, optional):
                An optional description for the policy
            name (str, optional): The Name of the new scan policy
            preferences (dict, optional):
                A dictionary of settings that override the defaults within a
                policy template.
            profile_name (str, optional):
                The profile of the scan.  Default is an empty string.
            remove_prefs (list, optional):
                A list of preferences to remove from the policy.
            owner_id (int, optional):
                Define who shall own the policy by that user's integer identifer
            tags (str, optional):
                An optional tag identifier for the policy
            template_id (int, optional): 
                The identifier of the policy template to use.  If none is
                specified, the default id for the "Advanced Policy" will be
                used.
            xccdf (bool, optional):
                Should XCCDF results be generated?  The default is False.
            
        Returns:
            dict: The updated scan policy resource.
        
        Examples:
            An example advanced policy with all of the default preferences.

            >>> sc.policies.edit(10001,
            ...     name='Updated Example Advanced Policy')

            To remove a preference, you would perform the following:

            >>> sc.policies.edit(10001,
            ...     remove_prefs=['scan_malware'])
        '''
        policy = self._constructor(**kw)

        # If remove_prefs is specified, then we will want to validate and move
        # the values over to the camelCase equiv.
        if 'remove_prefs' in policy:
            policy['removePrefs'] = [self._check('remove:{}'.format(a), a, str)
                for a in self._check('remove_prefs', policy['remove_prefs'], list)]
            del(policy['remove_prefs'])

        return self._api.patch('policy/{}'.format(
            self._check('id', id, int)), json=policy).json()['response']
    
    def delete(self, id):
        '''
        Removes a configured scan policy.

        + `SC Scan Policy Delete <https://docs.tenable.com/sccv/api/Scan-Policy.html#policy_id_DELETE>`_

        Args:
            id (int): The unique identifier for the policy to remove.
        
        Returns:
            str: The empty response from the API.
        
        Examples:
            >>> sc.policies.delete(10001)
        '''
        return self._api.delete('policy/{}'.format(
            self._check('id', id, int))).json()['response']
    
    def copy(self, id, name=None):
        '''
        Clones the specified scan policy

        + `SC Scan Policy Copy <https://docs.tenable.com/sccv/api/Scan-Policy.html#ScanPolicyRESTReference-/policy/{id}/copy>`_

        Args:
            id (int): The unique identifier for the source policy to clone. 
            name (str, optional): The name of the new policy. 
        
        Returns:
            dict: The scan policy resource record for the newly created policy.
        
        Examples:
            >>> policy = sc.policies.copy(10001)
            >>> pprint(policy)
        '''
        payload = dict()
        if name:
            payload['name'] = self._check('name', name, str)
        return self._api.post('policy/{}/copy'.format(
            self._check('id', id, int)), json=payload).json()['response']
    
    def export_policy(self, id, fobj=None):
        '''
        Export the specified scan policy

        + `SC Scan Policy Export <https://docs.tenable.com/sccv/api/Scan-Policy.html#ScanPolicyRESTReference-/policy/{id}/export>`_

        Args:
            id (int): The unique identifier for the scan policy to export.
            fobj (FileObject, optional):
                The file-like object to write the resulting file into.  If
                no file-like object is provided, a BytesIO objects with the
                downloaded file will be returned.  Be aware that the default
                option of using a BytesIO object means that the file will be
                stored in memory, and it's generally recommended to pass an
                actual file-object to write to instead.

        Returns:
            FileObject: The file-like object with the resulting export.

        Examples:
            >>> with open('example_policy.xml', 'wb') as fobj:
            ...     sc.policies.export_policy(1001, fobj)
        '''
        resp = self._api.post('policy/{}/export'.format(
            self._check('id', id, int)), stream=True)

        # if no file-like object was passed, then we will instantiate a BytesIO
        # object to push the file into.
        if not fobj:
            fobj = BytesIO()

        # Lets stream the file into the file-like object...
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                fobj.write(chunk)
        fobj.seek(0)
        return fobj
    
    def import_policy(self, name, fobj, description=None, tags=None):
        '''
        Imports a scan policy into Tenable.sc

        + `SC Scan Policy Import <https://docs.tenable.com/sccv/api/Scan-Policy.html#ScanPolicyRESTReference-/policy/import>`_

        Args:
            name (str): The name of the imported scan policy. 
            fobj (FileObject): The file-like object containing the scan policy.
            description (str, optional): A description for the scan policy.
            tags (str, optional): A tag for the scan policy.
        
        Returns:
            str: An empty response from the API.
        
        Examples:
            >>> with open('example_policy.xml', 'rb') as fobj:
            ...     sc.policies.import_policy('Example Policy', fobj)
        '''
        payload = {'name': self._check('name', name, str)}
        if description:
            payload['description'] = self._check('description', description, str)
        if tags:
            payload['tags'] = self._check('tags', tags, str)
        payload['filename'] = self._api.files.upload(fobj)
        return self._api.post('policy/import', json=payload).json()['response']
    
    def share(self, id, *groups):
        '''
        Shares the policy with other user groups.

        + `SC Scan Policy Share <https://docs.tenable.com/sccv/api/Scan-Policy.html#ScanPolicyRESTReference-/policy/{id}/share>`_

        Args:
            id (int): The unique identifier for the scan policy to share. 
            *groups (int): The list of user group ids to share the policy to. 
        
        Returns:
            dict: The updated scan policy resource.
        
        Examples:
            Share the scan policy with groups 1, 2, and 3:

            >>> sc.policies.share(10001, 1, 2, 3)
        '''
        return self._api.post('policy/{}/share'.format(
            self._check('id', id, int)), json={'groups': [{
                'id': self._check('group_id', i, int)} 
                    for i in groups]}).json()['response']
    
    def tags(self):
        '''
        Returns the list of unique tags associated to scan policies.

        + `SC Scan Policy Tags <https://docs.tenable.com/sccv/api/Scan-Policy.html#ScanPolicyRESTReference-/policy/tag>`_

        Returns:
            list: The list of unique tags
        
        Examples:
            >>> tags = sc.policies.tags()
            >>> pprint(tags)
        '''
        return self._api.get('policy/tag').json()['response']