'''
Users
=====

Methods described in this section relate to the users API.
These methods can be accessed at ``Nessus.users``.

.. rst-class:: hide-signature
.. autoclass:: UsersAPI
    :members:
'''
from typing import List, Dict, Optional
from typing_extensions import Literal
from restfly.utils import dict_clean
from tenable.base.endpoint import APIEndpoint


class UsersAPI(APIEndpoint):
    _path = 'users'
    
    def create(self,
               username: str,
               password: str,
               permissions: int,
               type: Literal['local', 'ldap'] = 'local',
               name: Optional[str] = None,
               email: Optional[str] = None
               ) -> Dict:
        '''
        Creates a new user
        
        Args:
            username (str): The unique username
            password (str): The user's password
            permissions (int): 
                The permission level for the user.  Basic users are ``16``,
                regular Users are ``32``, and administrators are ``64``.
            type (str, optional): 
                The type of user account to create.  The default is ``local``
            name (str, optional): A friendly name for the user
            email (str, optional): The user's email address
        
        Returns:
            Dict:
                The created user object
        
        Example:
        
            >>> nessus.users.create(username='example', 
            ...                     password='s3cr3tsqu1rr3l',
            ...                     permissions=32,
            ...                     name='Example User',
            ...                     email='example@company.com'
            ...                     )
        '''
        return self._post(json=dict_clean({
            'username': username,
            'password': password,
            'permissions': permissions,
            'type': type,
            'name': name,
            'email': email
        }))
    
    def delete(self, user_id: int) -> None:
        '''
        Deletes the specified user
        
        Args:
            user_id (int): The id of the user to delete
        
        Example:
        
            >>> nessus.users.delete(1)
        '''
        self._delete(f'{user_id}')
    
    def delete_many(self, user_ids: List[int]) -> None:
        '''
        Deletes many users
        
        Args:
            user_ids (list[int]): The list of user ids to delete
        
        Example:
        
            >>> nessus.users.delete_many([1, 2, 3])
        '''
        self._delete(json={'ids': user_ids})
    
    def details(self, user_id: int) -> Dict:
        '''
        Retrieves the specified user object
        
        Args:
            user_id (int): The id of the user to fetch
        
        Returns:
            Dict:
                The user object
        
        Example:
            
            >>> nessus.users.details(1)
        '''
        return self._get(f'{user_id}')
    
    def edit(self, 
             user_id: int, 
             permissions: int,
             name: Optional[str] = None,
             email: Optional[str] = None
             ) -> Dict:
        '''
        Updates the specified user object
        
        Args:
            user_id (int): The id of the user to update
            permissions (int): The permissions settings for the user
            name (str, optional): The user's friendly name
            email (str, optional): The user's email address
        
        Returns:
            Dict:
                The updates user object
        
        Example:
            
            >>> nessus.users.edit(1, 32, name='Updated User')
        '''
        return self._put(f'{user_id}', json=dict_clean({
            'permissions': permissions,
            'name': name,
            'email': email
        }))
    
    def list(self) -> List[Dict]:
        '''
        Retrieves the list of users configured in the system
        
        Returns:
            List[Dict]:
                List of user objects
        
        Example:
        
            >>> for user in nessus.users.list():
            ...     print(user)
        '''
        return self._get()['users']
    
    def chpasswd(self, user_id: int, password: str) -> None:
        '''
        Change the specified user's password
        
        Args:
            user_id (int): The user to update
            password (str): The new password
        
        Example:
            
            >>> nessus.users.chpasswd(1, 'n3wp@ssw0rd')
        '''
        self._put(f'{user_id}/chpasswd', json={
            'password': password
        })
    
    def api_keys(self, user_id: int) -> Dict:
        '''
        Generates API Keys for the specified user
        
        Args:
            user_id (int): The id of the user to generate keys for
        
        Returns:
            Dict:
                The new API Keys
        
        Example:
            
            >>> nessus.users.api_keys(1)
        '''
        return self._put(f'{user_id}/keys')