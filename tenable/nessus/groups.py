'''
Groups
======

Methods described in this section relate to the groups API.
These methods can be accessed at ``Nessus.groups``.

.. rst-class:: hide-signature
.. autoclass:: GroupsAPI
    :members:
'''
from tenable.base.endpoint import APIEndpoint
from typing import List, Dict


class GroupsAPI(APIEndpoint):
    _path = 'groups'
    
    def add_user(self, group_id: int, user_id: int) -> None:
        '''
        Adds a user to the group
        
        Args:
            group_id (int): The group id
            user_id (int): The user id
        
        Example:
            
            >>> nessus.groups.add_user(group_id, user_id)
        '''
        self._post(f'{group_id}/users/{user_id}')
    
    def create(self, name: str) -> Dict:
        '''
        Creates a new group
        
        Args:
            name (str): The name of the new group
        
        Returns:
            Dict:
                The new group object
        
        Example:
        
            >>> nessus.groups.create('Example Group')
        '''
        return self._post(json={'name': name})
    
    def delete(self, group_id: int) -> None:
        '''
        Deletes a group
        
        Args:
            group_id (int): The id of the group to delete
        
        Example:
            
            >>> nessus.groups.delete(group_id)
        '''
        self._delete(f'{group_id}')
    
    def delete_many(self, group_ids: List[int]) -> None:
        '''
        Deletes many groups
        
        Args:
            group_ids (list[int]): The list of group ids to delete
        
        Example:
            
            >>> nessus.groups.delete_many([group_1, group_2, group_3])
        '''
        self._delete(json={'ids': group_ids})
    
    def remove_user(self, group_id: int, user_id: int) -> None:
        '''
        Removes a user from the specified group
        
        Args:
            group_id (int): The group to modify
            user_id (int): The user to remove
        
        Example:
            
            >>> nessus.groups.remove_user(group_id, user_id)
        '''
        self._delete(f'{group_id}/users/{user_id}')
    
    def edit(self, group_id: int, name: str) -> Dict:
        '''
        Edits the specified group
        
        Args:
            group_id (int): The group to edit
            name (str): The new name for the group
            
        Returns:
            Dict:
                The updated group object
        
        Example:
            
            >>> nessus.groups.edit(group_id, name='Updated Name')
        '''
        return self._put(f'{group_id}', json={'name': name})
    
    def list(self) -> List[Dict]:
        '''
        Gets the list of groups
        
        Returns:
            List:
                List of group objects
        
        Example:
        
            >>> for group in nessus.groups.list():
            ...     print(group)
        '''
        return self._get()['groups']
    
    def list_users(self, group_id: int) -> List[Dict]:
        '''
        Gets the list of users associated to the specified group
        
        Args:
            group_id (int): The group to request members for
        
        Returns:
            List:
                The list of users associated to the group specified.
        
        Example:
            
            >>> for user in nessus.groups.list_users(group_id):
            ...     print(user)
        '''
        return self._get(f'{group_id}/users')['users']