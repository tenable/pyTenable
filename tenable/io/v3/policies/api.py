'''
Policies
========

The following methods allow for interaction into the Tenable.io
:devportal:`policies <policies>` API.

Methods available on ``tio.v3.policies``:

.. rst-class:: hide-signature
.. autoclass:: PoliciesAPI
    :members:
'''
from io import BytesIO
from typing import BinaryIO, Dict, List, Optional, Union

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.policies.schema import PoliciesSchema

# from tenable.utils import dict_merge, policy_settings


class PoliciesAPI(ExploreBaseEndpoint):
    '''
    This class contain all methods related to Policies Endpoint
    '''

    _path = 'api/v3/policies'
    _conv_json = True
    _schema = PoliciesSchema()

    def templates(self):
        '''
        returns a dictionary of the scan policy templates using the
        format of dict['name'] = 'UUID'.  This is useful for being able to
        define scan policy templates w/o having to remember the UUID for each
        individual one.
        '''
        raise NotImplementedError(
            'This functionality will be implemented after Editor'
            ' module is completed'
            )
        # policies = dict()
        # for item in self._api.v3.editor.template_list('policy'):
        #     policies[item['name']] = item['uuid']
        # return policies

    def template_details(self, name: str) -> Dict:
        '''
        Calls the editor API and parses the policy template config to return a
        document that closely matches what the API expects to be POSTed
        or PUTed via the policy create and configure methods.  The compliance
        audits and credentials are populated into the 'current'
        sub-document for the relevant resources.

        Args:
            name (str): The name of the scan template.

        Returns:
            :obj:`dict`:
                The policy configuration resource.

        Examples:
            >>> template = tio.v3.policies.template_details('basic')
            >>> pprint(template)

        Please note that template_details is reverse-engineered from the
        responses from the editor API and isn't guaranteed to work.
        '''

        raise NotImplementedError(
            'This functionality will be implemented after Editor'
            'module is completed'
            )
        # Get the policy template UUID
        # tmpl = self.templates()
        # tmpl_uuid = tmpl[self._check('name', name, str, choices=tmpl.keys())]

        # # Get the editor object
        # editor = self._api.v3.editor.template_details('policy', tmpl_uuid)

        # # define the initial skeleton of the scan object
        # scan = {
        #     'settings': policy_settings(editor['settings']),
        #     'uuid': editor['uuid']
        # }

        # # graft on the basic settings that aren't stored in any input
        # sections.
        # for item in editor['settings']['basic']['groups']:
        #     for setting in item.keys():
        #         if setting not in ['name', 'title', 'inputs', 'sections']:
        #             scan['settings'][setting] = item[setting]

        # if 'credentials' in editor:
        #     # if the credentials sub-document exists, then lets walk down the
        #     # credentials dataset
        #     scan['credentials'] = {
        #         'current': self._api.v3.editor.parse_creds(
        #             editor['credentials']['data'])
        #     }

        #     # We also need to gather the settings from the various credential
        #     # settings that are unique to the scan.
        #     for ctype in editor['credentials']['data']:
        #         for citem in ctype['types']:
        #             if 'settings' in citem and citem['settings']:
        #                 scan['settings'] = dict_merge(
        #                     scan['settings'], policy_settings(
        #                         citem['settings']))

        # if 'compliance' in editor:
        #     # if the audits sub-document exists, then lets walk down the
        #     # audits dataset.
        #     scan['compliance'] = {
        #         'current': self._api.v3.editor.parse_audits(
        #             editor['compliance']['data'])
        #     }

        #     # We also need to add in the "compliance" settings into the scan
        #     # settings.
        #     for item in editor['compliance']['data']:
        #         if 'settings' in item:
        #             scan['settings'] = dict_merge(
        #                 scan['settings'], policy_settings(
        #                     item['settings']))

        # if 'plugins' in editor:
        #     # if the plugins sub-document exists, then lets walk down the
        #     # plugins dataset.
        #     scan['plugins'] = self._api.v3.editor.parse_plugins(
        #         'policy', editor['plugins']['families'], tmpl_uuid)

        # # return the scan document to the caller.
        # return scan

    def configure(self, id: int, policy: Dict) -> None:
        '''
        Configures an existing policy.

        :devportal:`policies: configure <policies-configure>`

        Args:
            id (int): The policy unique identifier.
            policy (dict):
                The updated policy definition to push into Tenable.io. As these
                policies can be quite complex, please refer to the
                documentation in the policies: configure page (linked above).

        Returns:
            :obj:`None`:
                Policy successfully modified.

        Examples:
            >>> policy = tio.v3.policies.details(1)
            >>> policy['settings']['name'] = 'Updated Policy Name'
            >>> tio.v3.policies.configure(1, policy)
        '''
        policy = self._schema.dump(
            self._schema.load(policy)
            )
        self._put(f'{id}', json=policy)

    def copy(self, id: int) -> Dict:
        '''
        Duplicates a scan policy and returns the copy.

        :devportal:`policies: copy <policies-copy>`

        Args:
            id (int): The unique identifier of the policy you wish to copy.

        Returns:
            :obj:`dict`:
                A dictionary containing the name and id of the policy copy.

        Example:
            >>> policy = tio.v3.policies.copy(1)
        '''
        return self._post(f'{id}/copy')

    def create(self, policy: Dict) -> Dict:
        '''
        Creates a new scan policy based on the policy dictionary passed.

        :devportal:`policies: configure <policies-configure>`

        Args:
            policy (dict):
                The policy definition to push into Tenable.io. As these
                policies can be quite complex, please refer to the
                documentationin the policies: configure page (linked above).

        Returns:
            :obj:`dict`:
                A dictionary containing the name and id of the new policy.

        Examples:
            >>> policy = tio.v3.policies.template_details('basic')
            >>> policy['settings']['name'] = 'New Scan Policy'
            >>> info = tio.v3.policies.create(policy)
        '''
        policy = self._schema.dump(
            self._schema.load(policy)
            )
        return self._post(json=policy)

    def delete(self, id: int) -> None:
        '''
        Delete a custom policy.

        :devportal:`policies: delete <policies-delete>`

        Args:
            id (int): The unique identifier of the policy to delete.

        Returns:
            :obj:`None`:
                The policy was successfully deleted.

        Examples:
            >>> tio.v3.policies.delete(1)
        '''
        self._delete(f'{id}')

    def details(self, id: int) -> Dict:
        '''
        Retrieve the details for a specific policy.

        :devportal:`policies: details <policies-details>`

        Args:
            id (int): The unique identifier of the policy.

        Returns:
            :obj:`dict`:
                The dictionary definition of the policy.

        Examples:
            >>> policy = tio.v3.policies.details(1)
        '''
        return self._get(f'{id}')

    def policy_import(self, fobj: BinaryIO) -> Dict:
        '''
        Imports a policy into Tenable.io.

        :devportal:`policies: import <policies-import>`

        Args:
            fobj (FileObject):
                The file object of the scan policy you wish to import.

        Returns:
            :obj:`dict`:
                The dictionary of the imported policy.

        Examples:
            >>> with open('example.nessus') as policy:
            ...     tio.v3.policies.policy_import(policy)
        '''
        fid = self._api.v3.vm.files.upload(fobj)
        return self._post('import', json={'file': fid})

    def policy_export(
        self,
        id: int,
        fobj: Optional[Union[BytesIO, BinaryIO]] = None
    ) -> Union[BytesIO, BinaryIO]:
        '''
        Exports a specified policy from Tenable.io.

        :devportal:`policies: export <policies-export>`

        Args:
            id (int): The unique identifier of the policy to export.
            fobj (FileObject, optional):
                A file-like object to write the contents of the policy to.  If
                none is provided a BytesIO object will be returned with the
                policy.

        Returns:
            :obj:`FileObject`:
                A file-like object containing the contents of the policy
                in XML format.

        Examples:
            >>> with open('example.nessus', 'wb') as policy:
            ...     tio.v3.policies.policy_export(1, policy)
        '''
        # If no file object was given to us, then lets create a new BytesIO
        # object to dump the data into.
        if not fobj:
            fobj = BytesIO()

        # make the call to get the file.
        resp = self._get(f'{id}/export', stream=True)

        # Stream the data into the file.
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                fobj.write(chunk)
        fobj.seek(0)
        resp.close()

        # return the FileObject.
        return fobj

    def search(self, *kw) -> List:
        '''
        List the available custom policies based on given parameters.

        :devportal:`policies: list <policies-search>`

        Returns:
            :obj:`list`:
                List of policy resource documents.

        Examples:
            >>> for policy in tio.v3.policies.search():
            ...     pprint(policy)
        '''
        # return self._api.get('policies').json()['policies']
        raise NotImplementedError('Search functionality is not implemented')
