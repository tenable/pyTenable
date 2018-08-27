from tenable.tenable_io.base import TIOEndpoint
from io import BytesIO

class PoliciesAPI(TIOEndpoint):
    def templates(self):
        '''
        returns a dictionary of the scan policy templates using the
        format of dict['name'] = 'UUID'.  This is useful for being able to
        define scan policy templates w/o having to remember the UUID for each
        individual one.
        '''
        policies = dict()
        for item in self._api.editor.list('policy'):
            policies[item['name']] = item['uuid']
        return policies

    def template_details(self, name):
        '''
        Calls the editor API and parses the policy template config to return a
        document that closely matches what the API expects to be POSTed or PUTed
        via the policy create and configure methods.  The compliance audits and
        credentials are populated into the 'current' sub-document for the
        relevent resources.

        Args:
            name (str): The name of the scan .

        Returns:
            dict: The policy configuration resource.

        Please note that template_details is reverse-engineered from the 
        responses from the editor API and isn't guaranteed to work. 
        '''

        # Get the policy template UUID
        tmpl = self.templates()
        tmpl_uuid = tmpl[self._check('name', name, str, choices=tmpl.keys())]

        # Get the editor object
        editor = self._api.get('editor/policy/{}'.format(
            self._check('scan_id', scan_id, int))).json()

        # define the initial skeleton of the scan object
        scan = {
            'settings': self._api.editor.parse_vals(editor['settings']),
            'uuid': editor['uuid']
        }

        # graft on the basic settings that aren't stored in any input sections.
        for item in editor['settings']['basic']['groups']:
            for setting in item.keys():
                if setting not in ['name', 'title', 'inputs']:
                    scan['settings'][setting] = item[setting]

        if 'credentials' in editor:
            # if the credentials sub-document exists, then lets walk down the
            # credentials dataset
            scan['credentials'] = {
                'current': self._api.editor.parse_creds(
                    editor['credentials']['data'])
            }

            # We also need to gather the settings from the various credential
            # settings that are unique to the scan.
            for ctype in editor['credentials']['data']:
                for citem in ctype['types']:
                    if 'settings' in citem and citem['settings']:
                        scan['settings'] = dict_merge(
                            scan['settings'], self._api.editor.parse_vals(
                                citem['settings']))

        if 'compliance' in editor:
            # if the audits sub-document exists, then lets walk down the
            # audits dataset.
            scan['compliance'] = {
                'current': self._api.editor.parse_audits(
                    editor['compliance']['data'])
            }

            # We also need to add in the "compliance" settings into the scan
            # settings.
            for item in editor['compliance']['data']:
                if 'settings' in item:
                    scan['settings'] = dict_merge(
                        scan['settings'], self._api.editor.parse_vals(
                            item['settings']))

        if 'plugins' in editor:
            # if the plugins sub-document exists, then lets walk down the
            # plugins dataset.
            scan['plugins'] = self._api.editor.parse_plugins(
                editor['plugins']['families'], scan_id)

        # We next need to do a little post-parsing of the ACLs to find the
        # owner and put ownder_id attribute into the appropriate location.
        for acl in scan['settings']['acls']:
            if acl['owner'] == 1:
                scan['settings']['owner_id'] = acl['id']

        # return the scan document to the caller.
        return scan

    def configure(self, id, policy):
        '''
        `policies: configure <https://cloud.tenable.com/api#/resources/policies/configure>`_

        Args:
            id (int): The policy unique identifier.
            policy (dict):
                The updated policy definition to push into Tenable.io.  As these
                policies can be quite complex, please refer to the documentation
                in the policies: configure page (linked above).

        Returns:
            None: Policy successfully modified.
        '''
        self._api.put('policies/{}'.format(self._check('id', id, int)), 
            json=self._check('policy', policy, dict))

    def copy(self, id):
        '''
        `policies: copy <https://cloud.tenable.com/api#/resources/policies/copy>`_

        Args:
            id (int): The unique identifier of the policy you wish to copy.

        Returns:
            dict: A dictionary containing the name and id of the policy copy.
        '''
        return self._api.post('policies/{}/copy'.format(
            self._check('id', id, int))).json()

    def create(self, policy):
        '''
        `policies: configure <https://cloud.tenable.com/api#/resources/policies/configure>`_

        Args:
            policy (dict):
                The policy definition to push into Tenable.io.  As these
                policies can be quite complex, please refer to the documentation
                in the policies: configure page (linked above).

        Returns:
            dict: A dictionary containing the name and id of the new policy.
        '''
        return self._api.post('policies', 
            json=self._check('policy', policy, dict)).json()

    def delete(self, id):
        '''
        `policies: delete <https://cloud.tenable.com/api#/resources/policies/delete>`_

        Args:
            id (int): The unique identifier of the policty to delete.

        Returns:
            None: The policy was successfully deleted.
        '''
        self._api.delete('policies/{}'.format(self._check('id', id, int)))

    def details(self, id):
        '''
        `policies: details <https://cloud.tenable.com/api#/resources/policies/details>`_

        Args:
            id (int): The unique identifier of the policy.

        Returns:
            dict: The dictionary definition of the policy.
        '''
        return self._api.get('policies/{}'.format(
            self._check('id', id, int))).json()

    def policy_import(self, fobj):
        '''
        `policies: import <https://cloud.tenable.com/api#/resources/policies/import>`_

        Args:
            fobj (FileObject): 
                The file object of the scan policy you wish to import.

        Returns:
            dict: The dictionary of the imported policy.
        '''
        fid = self._api.file.upload(fobj)
        return self._api.post('policies/import', json={'file': fid}).json()

    def policy_export(self, id, fobj=None):
        '''
        `policies: export <https://cloud.tenable.com/api#/resources/policies/export>`_

        Args:
            id (int): The unique identifier of the policy to export.
            fobj (FileObject, optional):
                A file-like object to write the contents of the policy to.  If
                none is provided a BytesIO object will be returned with the
                policy.

        Returns:
            FileObject: A file-like object containing the contents of the policy
            in XML format.
        '''
        # If no file object was givent to us, then lets create a new BytesIO
        # object to dump the data into.
        if not fobj:
            fobj = BytesIO()

        # make the call to get the file.
        resp = self._api.get('policies/{}/export'.format(
            self._check('id', id, int)), stream=True)

        # Stream the data into the file.
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                fobj.write(chunk)
        fobj.seek(0)

        # return the FileObject.
        return fobj

    def list(self):
        '''
        `policies: list <https://cloud.tenable.com/api#/resources/policies/list>`_

        Returns:
            list: List of policy resource documents.
        '''
        return self._api.get('policies').json()['policies']
