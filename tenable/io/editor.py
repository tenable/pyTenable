'''
editor
======

The following methods allow for interaction into the Tenable.io 
`editor <https://cloud.tenable.com/api#/resources/editor>`_ 
API endpoints.  While these endpoints are pythonized for completeness within
pyTenable, the Editor API endpoints should generally be avoided unless absolutely
necessary.  These endpoints are used to drive the Tenable.io UI, and not
designed to be used programmatically.

Methods available on ``io.editor``:

.. rst-class:: hide-signature
.. autoclass:: EditorAPI

    .. automethod:: audits
    .. automethod:: details
    .. automethod:: edit
    .. automethod:: list
    .. automethod:: plugin_description
'''
from .base import TIOEndpoint
from tenable.utils import dict_merge, policy_settings
from io import BytesIO

class EditorAPI(TIOEndpoint):
    def parse_creds(self, data):
        '''
        Walks through the credential data list and returns the configured 
        settings for a given scan policy/scan
        '''
        resp = dict()
        for dtype in data:
            for item in dtype['types']:
                if len(item['instances']) > 0:
                    for i in item['instances']:
                        # Get the settings from the inputs.
                        settings = policy_settings(i)
                        settings['id'] = i['id']
                        settings['summary'] = i['summary']

                        if dtype['name'] not in resp:
                            # if the Datatype doesn't exist yet, create it.
                            resp[dtype['name']] = dict()

                        if item['name'] not in resp[dtype['name']]:
                            # if the data subtype doesn't exist yet,
                            # create it. 
                            resp[dtype['name']][item['name']] = list()

                        # Add the configured settings to the key-value
                        # dictionary
                        resp[dtype['name']][item['name']].append(settings)
        return resp

    def parse_audits(self, data):
        '''
        Walks through the compliance data list and returns the configured
        settings for a given policy/scan
        '''
        resp = {
            'custom': dict(),
            'feed': dict()
        }

        for atype in data:
            for audit in atype['audits']:
                if audit['free'] == 0:
                    if audit['type'] == 'custom':
                        # if the audit is a custom-uploaded file, then we
                        # need to return the data using the format below,
                        # which appears to be how the UI sends the data.
                        fn = audit['summary'].split('File: ')[1]
                        resp['custom'].append({
                            'id': audit['id'],
                            'category': atype['name'],
                            'file': fn,
                            'variables': {
                                'file': fn,
                            }
                        })
                    else:
                        # if we're using a audit file from the feed, then
                        # we will want to pull all of the parameterized
                        # variables with the set values and store them in
                        # the variables dictionary.
                        if atype['name'] not in resp['feed']:
                            resp['feed'][atype['name']] = list()
                        resp['feed'][atype['name']].append({
                            'id': audit['id'],
                            'variables': policy_settings(audit)
                        })
        return resp 

    def parse_plugins(self, families, id, callfmt='editor/{id}/families/{fam}'):
        '''
        Walks through the plugin settings and will return the the configured
        settings for a given scan/policy
        '''
        resp = dict()

        for family in families:
            if families[family]['status'] != 'mixed':
                # if the plugin family is wholly enabled or disabled, then
                # all we need to set is the status.
                resp[family] = {'status': families[family]['status']}
            else:
                # if the plugin family is set to mixed, we will need to get
                # the currently enabled status of every plugin within the
                # mixed families.  To do so, we will need to query the
                # scan editor for each mixed family, getting the plugin
                # listing w/ status an interpreting that into a simple
                # dictionary of plugin_id:status.
                plugins = dict()
                plugs = self._api.get(callfmt.format(
                    id=id, fam=families[family]['id'])).json()['plugins']
                for plugin in plugs:
                    plugins[plugin['id']] = plugin['status']
                resp[family] = {
                    'mixedDefault': 'enabled',
                    'status': 'mixed',
                    'individual': plugins,
                }
        return resp

    def audits(self, etype, object_id, file_id, fobj=None):
        '''
        Retrieves an audit file from Tenable.io

        `editor: audits <https://cloud.tenable.com/api#/resources/editor/audits>`_

        Args:
            etype (str):
                The type of template to retrieve.  Must be either ``scan`` or
                ``policy``.
            object_od (int):
                The unique identifier of the object.
            file_id (int):
                The unique identifier of the file to export.
            fobj (FileObject):
                An optional File-like object to write the file to.  If none is
                provided a BytesIO object will be returned.

        Returns:
            FileObject: A File-like object of of the audit file.
        '''
        # If no file object was given to us, then lets create a new BytesIO
        # object to dump the data into.
        if not fobj:
            fobj = BytesIO()

        # Now we need to make the actual call.
        resp = self._api.get(
            'editor/{}/{}/audits/{}'.format(
                self._check('etype', etype, str, choices=['scan', 'policy']),
                self._check('object_id', object_id, int),
                self._check('file_id', file_id, int)
            ), stream=True)

        # Once we have made the call, stream the data into the file in 1k chunks.
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                fobj.write(chunk)
        fobj.seek(0)

        # lastly return the file object.
        return fobj

    def details(self, etype, uuid):
        '''
        Retrieves details about a specific object.

        `editor: details <https://cloud.tenable.com/api#/resources/editor/details>`_

        Args:
            etype (str):
                The type of template to retrieve.  Must be either ``scan`` or
                ``policy``.
            uuid (str):
                The UUID (unique identifier) for the template.

        Returns:
            dict: Details on the requested template
        '''
        return self._api.get(
            'editor/{}/templates/{}'.format(
                self._check('etype', etype, str, choices=['scan', 'policy']),
                self._check('uuid', uuid, str)
            )).json()

    def edit(self, etype, id):
        '''
        Edits an object.

        `editor: edit <https://cloud.tenable.com/api#/resources/editor/edit>`_

        Args:
            etype (str):
                The type of object to retrieve.  Must be either ``scan`` or
                ``policy``.
            id (int):
                The unique identifier of the object.

        Returns:
            dict: Details of the requested object
        '''
        return self._api.get(
            'editor/{}/{}'.format(
                self._check('etype', etype, str, choices=['scan', 'policy']),
                self._check('id', id, int)
            )).json()

    def list(self, etype):
        '''
        List objects.

        `editor: list <https://cloud.tenable.com/api#/resources/editor/list>`_

        Args:
            etype (str):
                The type of object to retrieve.  Must be either ``scan`` or
                ``policy``.

        Returns:
            list: Listing of template records.
        '''
        return self._api.get(
            'editor/{}/templates'.format(
                self._check('etype', etype, str, choices=['scan', 'policy'])
            )).json()['templates']

    def plugin_description(self, policy_id, family_id, plugin_id):
        '''
        Retrieves the plugin description for the specified plugin.

        `editor: plugin-description <https://cloud.tenable.com/api#/resources/editor/plugin-description>`_

        Args:
            policy_id (int):
                The identifier of the policy.
            family_id (int):
                The identifier of the plugin family.
            plugin_id (int):
                The identifier of the plugin within the family.

        Returns:
            dict: Details of the plugin requested.
        '''
        return self._api.get(
            'editor/policy/{}/families/{}/plugins/{}'.format(
                self._check('policy_id', policy_id, int),
                self._check('family_id', family_id, int),
                self._check('plugin_id', plugin_id, int)
            )).json()['plugindescription']