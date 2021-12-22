'''
User-Templates
==============

The following methods allow for interaction into the Tenable.io
:devportal:`Web Application Scanning v3 user-templates <was-v2-templates>` API.

Methods available on ``tio.v3.was.user_templates``:

.. rst-class:: hide-signature
.. autoclass:: UserTemplatesAPI
    :members:
'''
from typing import Dict, List
from uuid import UUID

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.was.user_templates.schema import UserTemplateSchema
from tenable.utils import dict_clean


class UserTemplatesAPI(ExploreBaseEndpoint):
    _path = 'api/v3/was/user-templates'
    _conv_json = True

    def delete(self, user_template_id: UUID) -> None:
        '''
        Deletes the specified user-defined template.

        :devportal:`was templates: Get user-defined template details
        <was-v2-user-templates-details>`
        Note:
            You cannot delete a user-defined template if scan configurations
            currently use the template. You must delete any scan configuration
            using the template prior to deleting the template. You can delete
            # TODO: Link to config delete function here
            scan configurations with the DELETE /was/v2/configs/{config_id}
            endpoint.

        Args:
            user_template_id (UUID): The UUID of the user-defined template.

        Returns:
            :obj:`None`

        Examples:
            >>> (tio.v3.was.user_templates.
            ...     delete('d5b3cb1c-9c72-4974-a936-3dfbd2e2835e'))
        '''
        self._delete(f'{user_template_id}')

    def details(self, user_template_id: UUID) -> Dict:
        '''
        Returns details for a user-defined template. User-defined templates can
        be used to define scan configurations.

        :devportal:`was templates: Get user-defined template details
        <was-v2-user-templates-details>`

        Args:
            user_template_id (UUID): The UUID of the user-defined template.

        Returns:
            :obj:`dict`: The resource record of the user-defined template.

        Examples:
            >>> template = (tio.v3.was.user_templates.
            ...     details('d5b3cb1c-9c72-4974-a936-3dfbd2e2835e'))
            >>> pprint(template)
        '''
        return super().details(user_template_id)

    def search(self, **kwargs) -> None:
        '''
        Not Implemented
        '''
        raise NotImplementedError(
            'This method will be updated once ExploreSearchIterator is \
                implemented for v3'
        )

    def update(self,
               user_template_id: UUID,
               name: str,
               owner_id: UUID,
               default_permissions: str,
               results_visibility: str,
               permissions: List,
               description: str = None
               ) -> Dict:
        '''
        Updates the specified user-defined template.

        :devportal:`was templates: Update user-defined template
        <was-v2-user-templates-update>`

        Args:
            user_template_id (UUID): The UUID of the user-defined template.
            name (str): The name of the user-defined template.
            owner_id (UUID):
                The UUID of the owner of the user-defined template.
            default_permissions (str):
                The scan permissions level, as described in Permissions.
            results_visibility (str):
                The visibility of the results (private or dashboard).
            permissions (list): The permissions for the user-defined template.
            description (str, optional):
                The description for the user-defined template.

        Returns:
            :obj:`dict`: The resource record of the user-defined template.

        Examples:
            >>> template = tio.v3.was.user_templates.update(
            ...     user_template_id = 'd5b3cb1c-9c72-4974-a936-3dfbd2e2835e',
            ...     name = 'template_1',
            ...     owner_id = '3fa85f64-5717-4562-b3fc-2c963f66afa6',
            ...     default_permissions = 'no_access',
            ...     results_visibility = 'dashboard',
            ...     permissions = [
            ...         {
            ...             'entity': 'user',
            ...             'entity_id':
            ...                 '3fa85f64-5717-4562-b3fc-2c963f66afa6',
            ...             'permissions_id':
            ...                 '3fa85f64-5717-4562-b3fc-2c963f66afa6'
            ...         }
            ...     ]
            ...     description = 'Template for containing threat'
            ... )
            >>> pprint(template)
        '''
        payload = {
            'name': name,
            'owner_id': owner_id,
            'default_permissions': default_permissions,
            'results_visibility': results_visibility,
            'permissions': permissions,
            'description': description
        }
        schema = UserTemplateSchema()
        payload = dict_clean(schema.dump(schema.load(payload)))
        self._put(f'{user_template_id}', json=payload)
