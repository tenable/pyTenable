'''
Credentials
===========

The following methods allow for interaction into the Tenable.io
:devportal:`credentials <credentials>` API endpoints.

Methods available on ``tio.v3.vm.credentials``:

.. rst-class:: hide-signature
.. autoclass:: CredentialsAPI
    :members:
'''
from typing import BinaryIO, Dict, List, Optional
from uuid import UUID

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.vm.credentials.schema import (CredentialsCreateSchema,
                                                 CredentialsEditSchema)
from tenable.utils import dict_clean, dict_merge


class CredentialsAPI(ExploreBaseEndpoint):
    _path = 'api/v3/credentials'
    _conv_json = True

    def create(self, cred_name: str, cred_type: str,
               description: Optional[str] = None,
               permissions: Optional[List] = None,
               **settings: Optional[Dict]) -> str:
        '''
        Creates a new managed credential.

        :devportal:`credentials: create <credentials-create>`

        Args:
            cred_name (str):
                The name of the credential.
            cred_type (str):
                The type of credential to create.  For a list of values refer
                 to
                the output of the :py:meth:`types() <CredentialsAPI.types>`
                method.
            description (str, optional):
                A description for the credential.
            permissions (list, optional):
                A list of permissions (in either tuple or native dict format)
                detailing whom is allowed to use or edit this credential set.
                For the dictionary format, refer to the API docs.  The tuple
                format uses the customary ``(type, perm, id)`` format.

                Examples:
                    - ``('user', 32, user_id)``
                    - ``('group', 32, group_id)``
                    - ``('user', 'use', user_id)``

            **settings (dict, optional):
                Additional keywords passed will be added to the settings dict
                within the API call.  As this dataset can be highly variable,
                it will not be validated and simply passed as-is.

        Returns:
            :obj:`str`:
                The UUID of the newly created credential.

        Examples:
            >>> group_id = '00000000-0000-0000-0000-000000000000'
            >>> tio.v3.vm.credentials.create('SSH Account', 'SSH',
            ...     permissions=[('group', 'use', group_id)],
            ...     username='user1',
            ...     password='sekretsquirrel',
            ...     escalation_account='root',
            ...     escalation_password='sudopassword',
            ...     elevate_privileges_with='sudo',
            ...     bin_directory='/usr/bin',
            ...     custom_password_prompt='')
        '''

        create_schema = CredentialsCreateSchema()
        payload = dict_clean(dict(
            name=cred_name,
            description=description,
            type=cred_type,
            settings=settings,
            permissions=permissions
        ))
        payload = create_schema.dump(create_schema.load(payload))

        return self._post(json=payload)['id']

    def edit(self, cred_id: UUID, cred_name: Optional[str] = None,
             description: Optional[str] = None,
             permissions: Optional[List] = None,
             ad_hoc: Optional[bool] = None,
             **settings: Optional[Dict]
             ) -> bool:
        '''
        Creates a new managed credential.

        :devportal:`credentials: create <credentials-create>`

        Args:
            cred_id (UUID):
                Credentials uuid
            ad_hoc (bool, optional):
                Determines whether the credential is managed (``False``) or an
                embedded credential in a scan or policy (``True``).
            cred_name (str, optional):
                The name of the credential.
            description (str, optional):
                A description for the credential.
            permissions (list, optional):
                A list of permissions (in either tuple or native dict format)
                detailing whom is allowed to use or edit this credential set.
                For the dictionary format, refer to the API docs.  The tuple
                format uses the customary ``(type, perm, uuid)`` format.

                Examples:
                    - ``('user', 32, user_id)``
                    - ``('group', 32, group_id)``
                    - ``('user', 'use', user_id)``
                    - ``('group', 'edit', group_id)``

            **settings (dict, optional):
                Additional keywords passed will be added to the settings dict
                within the API call.  As this dataset can be highly variable,
                it will not be validated and simply passed as-is.

        Returns:
            :obj:`bool`:
                The status of the update process.

        Examples:
            >>> cred_id = '00000000-0000-0000-0000-000000000000'
            >>> tio.v3.vm.credentials.edit(cred_id,
            ...     password='sekretsquirrel',
            ...     escalation_password='sudopassword')
        '''
        current = self.details(cred_id)

        if not cred_name:
            cred_name = current.get('name')
        if not description:
            description = current.get('description')
        if not ad_hoc:
            ad_hoc = current.get('ad_hoc')

        settings = dict_merge(current.get('settings'), settings)
        edit_schema = CredentialsEditSchema()
        payload = dict_clean(dict(
            name=cred_name,
            description=description,
            ad_hoc=ad_hoc,
            permissions=permissions,
            settings=settings
        ))
        payload = edit_schema.dump(edit_schema.load(payload))
        return self._put(cred_id, json=payload)['updated']

    def details(self, id: UUID) -> Dict:
        '''
        Retrieves the details of the specified credential.

        :devportal:`credentials: details <credentials-details>`

        Args:
            id (UUID): The UUID of the credential to retrieve.

        Returns:
            :obj:`Dict`:
                The resource record for the credential.

        Examples:
            >>> cred_id = '00000000-0000-0000-0000-000000000000'
            >>> cred = tio.v3.vm.credentials.details(cred_id)
        '''
        return self._get(id)

    def delete(self, id: UUID) -> bool:
        '''
        Deletes the specified credential.

        :devportal:`credentials: delete <credentials-delete>`

        Args:
            id (UUID): The UUID of the credential to retrieve.

        Returns:
            :obj:`bool`:
                The status of the action.

        Examples:
            >>> cred_id = '00000000-0000-0000-0000-000000000000'
            >>> cred = tio.v3.vm.credentials.delete(cred_id)
        '''
        return self._delete(id)['deleted']

    def types(self) -> List:
        '''
        Lists all of the available credential types.

        :devportal:`credentials: list-types
        <credentials-list-credential-types>`

        Returns:
            :obj:`list`:
                A list of the available credential types and definitions.

        Examples:
            >>> cred_types = tio.v3.vm.credentials.types()
        '''
        return self._get('types')['credentials']

    def upload(self, fobj: BinaryIO) -> str:
        '''
        Uploads a file for use with a managed credential.

        :devportal:`credentials: upload <file-upload>`

        Args:
            fobj (FileObject):
                The file object intended to be uploaded into Tenable.io.

        Returns:
            :obj:`str`:
                The fileuploaded attribute
        '''

        # We will attempt to discover the name of the file stored within the
        # file object.  If the name of the file is successfully discovered, we
        # will generate a random uuid string and append it to the name.
        # Otherwise, we will generate a random uuid string to use instead.
        kw = {
            'files': {
                'Filedata': fobj
            }
        }

        return self._post('files', **kw)['fileuploaded']
