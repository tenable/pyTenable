'''
Policies
========

Methods described in this section relate to the files API.
These methods can be accessed at ``Nessus.policies``.

.. rst-class:: hide-signature
.. autoclass:: PoliciesAPI
    :members:
'''
from io import BytesIO
from typing import Optional, Dict, List
from tenable.base.endpoint import APIEndpoint


class PoliciesAPI(APIEndpoint):  # noqa PLC0115
    _path = 'policies'

    def copy(self, policy_id: int) -> Dict:
        '''
        Duplicates an existing scan policy.

        Args:
            policy_id (int): The id of the policy to clone.

        Returns:
            Dict:
                The cloned policy object.

        Example:

            >>> nessus.policies.copy(1)
        '''
        return self._post(f'{policy_id}/copy')

    def create(self, uuid: str, **kwargs) -> Dict:
        '''
        Creates a new scan policy using the provided settings.

        Args:
            uuid (str): The UUID for the editor template to use.
            **kwargs (dict): Additional settings to use to create the policy.

        Returns:
            Dict:
                Response object with identifying information on the new policy

        Example:

            >>> tmpl = '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65'
            >>> nessus.policies.create(tmpl_uuid, settings={
            ...     'name': 'Sample Policy'
            ... })
        '''
        kwargs['uuid'] = uuid
        return self._post(json=kwargs)

    def delete(self, policy_id: int) -> None:
        '''
        Deletes the specified scan policy.

        Args:
            policy_id (int): The id of the policy to delete.

        Example:

            >>> nessus.policies.delete(1)
        '''
        return self._delete(f'{policy_id}')

    def delete_many(self, policy_ids: List[int]) -> List[int]:
        '''
        Deletes the specified scan policies.

        Args:
            policy_ids (list[int]): The list of policy ids to delete.

        Example:

            >>> nessus.policies.delete_many([1, 2, 3])
        '''
        return self._delete(json={'ids': policy_ids})['deleted']

    def details(self, policy_id: int) -> Dict:
        '''
        Returns the details of the selected policy.

        Args:
            policy_id (int): The id of the policy to retrieve.

        Returns:
            Dict:
                The policy object.

        Example:

            >>> nessus.policies.details(1)
        '''
        return self._get(f'{policy_id}')

    def edit(self, policy_id: int, **kwargs) -> None:
        '''
        Updates an existing scan policy.

        Args:
            policy_id (int): The id of the policy to edit.
            **kwargs (dict): Attributes to be passed into the JSON body.

        Example:

            >>> policy = nessus.policies.details(1)
            >>> policy['settings']['name'] = 'Updated Policy'
            >>> nessus.policies.edit(1, **policy)
        '''
        return self._put(f'{policy_id}', json=kwargs)

    def import_policy(self, fobj: BytesIO) -> Dict:
        '''
        Imports the policy into the nessus scanner.

        Args:
            fobj (BytesIO): The file object containing the policy.

        Returns:
            Dict:
                The imported policy object.

        Example:

            >>> with open('policy.xml', 'rb') as policy:
            ...     nessus.policies.import_policy(policy)
        '''
        filename = self._api.files.upload(fobj)
        return self._post('import', json={'file': filename})

    def export_policy(self,
                      policy_id: int,
                      fobj: Optional[BytesIO] = None,
                      **kwargs
                      ) -> BytesIO:
        '''
        Export the specified policy and download it.

        Args:
            policy_id (int): The id of the policy to export.
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
        '''
        kwargs['fobj'] = fobj
        token = self._get(f'{policy_id}/export/prepare')['token']
        return self._api.tokens._fetch(token, **kwargs)  # noqa PLW0212

    def list(self,) -> List[Dict]:
        '''
        Lists the available policies.

        Returns:
            List[Dict]:
                List of policy objects.

        Example:

            >>> for policy in nessus.policies.list():
            ...     print(policy)
        '''
        return self._get()['policies']
