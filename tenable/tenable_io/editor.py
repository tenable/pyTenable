from tenable.base import APIEndpoint

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

class EditorAPI(APIEndpoint):
    def audits(self, etype, object_id, file_id, fobj=None):
        '''
        `editor: audits <https://cloud.tenable.com/api#/resources/editor/audits>`_

        Args:
            etype (str):
                The type of template to retreive.  Must be either ``scan`` or
                ``policy``.
            object_od (int):
                The unique identifier of the object.
            file_id (int):
                The unique identifier of the file to export.
            fobj (FileObject):
                An optional File-like object to write the file to.  If none is
                provided a StringIO object will be returned.

        Returns:
            FileObject: A File-like object of of the audit file.
        '''
        # If no file object was givent to us, then lets create a new StringIO
        # object to dump the data into.
        if not fobj:
            fobj = StringIO()

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
        `editor: details <https://cloud.tenable.com/api#/resources/editor/details>`_

        Args:
            etype (str):
                The type of template to retreive.  Must be either ``scan`` or
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
        `editor: edit <https://cloud.tenable.com/api#/resources/editor/edit>`_

        Args:
            etype (str):
                The type of object to retreive.  Must be either ``scan`` or
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
        `editor: list <https://cloud.tenable.com/api#/resources/editor/list>`_

        Args:
            etype (str):
                The type of object to retreive.  Must be either ``scan`` or
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