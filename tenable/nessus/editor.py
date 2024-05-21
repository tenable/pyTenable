'''
Editor
======

Methods described in this section relate to the the editor API.
These methods can be accessed at ``Nessus.editor``.

.. rst-class:: hide-signature
.. autoclass:: EditorAPI
    :members:
'''
from io import BytesIO
from typing import Dict, List
from typing_extensions import Literal
from tenable.base.endpoint import APIEndpoint


class EditorAPI(APIEndpoint):  # noqa PLC0115
    _path = 'editor'

    def export_audit(self,
                     object_type: Literal['scan', 'policy'],
                     object_id: int,
                     file_id: int,
                     **kwargs
                     ) -> BytesIO:
        '''
        Exports the given audit file. from the scan or policy

        Args:
            object_type (str):
                The object type (either scan or policy).
            object_id (int):
                The id of the object to export from.
            file_id (int):
                The id of the audit file to export.
            fobj (BytexIO, optional):
                The file object to write the exported file to.  If none is
                specified then a BytesIO object is written to in memory.
            chunk_size (int, optional):
                The chunk sizing for the download itself.
            stream_hook (callable, optional):
                Overload the default downloading behavior with a custom
                stream hook.
            hook_kwargs (dict, optional):
                keyword arguments to pass to the stream_hook callable in
                addition to the default passed params.

        Returns:
            BytesIO:
                The file object of the requested audit file.

        Example:

            >>> with open('example.audit', 'wb') as audit_file:
            ...     nessus.editor.export_audit('policy', 1, 1, fobj=audit_file)
        '''
        token = self._get(f'{object_type}/{object_id}/audits/{file_id}/prepare'
                          )['token']
        return self._api.tokens._fetch(token, **kwargs)  # noqa PLW0212

    def template_details(self,
                         object_type: Literal['scan', 'policy'],
                         template_uuid: str
                         ) -> Dict:
        '''
        Returns the template object requested.

        Args:
            object_type (str):
                The type of the object requested (either scan, or policy).
            template_uuid (str):
                The UUID of the template to fetch.

        Returns:
            Dict:
                The editor object for the requested template.

        Example:

            >>> nessus.editor.template_details(
            ...     'scan', '00000000-0000-0000-000000000000')
        '''
        return self._get(f'{object_type}/templates/{template_uuid}')

    def details(self,
                object_type: Literal['scan', 'policy'],
                object_id: int
                ) -> Dict:
        '''
        Returns the object requested.

        Args:
            object_type (str):
                The type of the object requested (either scan or policy).
            object_id (int):
                The id of the object to fetch.

        Returns:
            Dict:
                The editor object for the requested item.

        Example:

            >>> nessus.editor.details('scan', 1)
        '''
        return self._get(f'{object_type}/{object_id}')

    def template_list(self,
                      object_type: Literal['scan', 'policy']
                      ) -> List[Dict]:
        '''
        Returns the list of template objects.

        Args:
            object_type (str):
                The type of templates to return (either scan or policy).

        Returns:
            List[Dict]:
                List of template summaries.

        Example:

            >>> for tmpl in nessus.editor.template_list('scan'):
            ...     print(tmpl)
        '''
        return self._get(f'{object_type}/templates')['templates']

    def plugin_description(self,
                           policy_id: int,
                           family_id: int,
                           plugin_id: int
                           ) -> Dict:
        '''
        Returns the plugin description.

        Args:
            policy_id (int): The id of the policy to lookup.
            family_id (int): The id of the plugin family to lookup.
            plugin_id (int): The id of the plugin to lookup within the family.

        Returns:
            Dict:
                The plugin description.

        Example:

            >>> nessus.editor.plugin_description(1, 1, 19506)
        '''
        return self._get((f'policy/{policy_id}/'
                          f'families/{family_id}/'
                          f'plugins/{plugin_id}'
                          ))['plugindescription']
