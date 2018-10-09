from tenable.tenable_io.base import TIOEndpoint
from tenable.errors import UnexpectedValueError
from tenable.utils import dict_merge

class TargetGroupsAPI(TIOEndpoint):
    def create(self, name, members, **kw):
        '''
        `target-groups: create <https://cloud.tenable.com/api#/resources/target-groups/create>`_

        Args:
            name (str): The name of the target group
            members (list): 
                The members of the target group.  FQDNs, CIDRs, IPRanges, and
                individual IPs are supported.
            type (str, optional): 
                The type of target group to create.  Valid types are `user` and
                `system`.  The default if not specified is `system`.
            acls (list, optional):
                A list of ACLs defining how the asset list can be used.  For
                further information on how the ACL dictionaries should be
                written, please refer to the API documentation.
        
        Returns:
            dict: The resource record of the newly created target group.
        '''
        payload = {
            'name': self._check('name', name, str)
        }

        if 'acls' in kw:
            payload['acls'] = self._check('acls', kw['acls'], list)
        if 'type' in kw:
            payload['type'] = self._check('type', kw['type'], str,
                choices=['system', 'user'], default='system')
        if len(members) > 0:
            payload['members'] = ','.join(self._check('members', members, list))
        else:
            raise UnexpectedValueError('No members in members list')

        return self._api.post('target-groups', json=payload).json()

    def delete(self, id):
        '''
        `target-groups: delete <https://cloud.tenable.com/api#/resources/target-groups/delete>`_

        Args:
            id (int): The unique identifier for the target group.

        Returns:
            None: The target group was successfully deleted.
        '''
        self._api.delete('target-groups/{}'.format(self._check('id', id, int)))

    def details(self, id):
        '''
        `target-groups: details <https://cloud.tenable.com/api#/resources/target-groups/details>`_

        Args:
            id (int): The unique identifier for the target group.

        Returns:
            dict: The resource record for the target group.
        '''
        return self._api.get('target-groups/{}'.format(
            self._check('id', id, int))).json()

    def edit(self, id, **kw):
        '''
        `target-groups: edit <https://cloud.tenable.com/api#/resources/target-groups/edit>`_

        Args:
            id (int): The unique identifier for the target group.
            name (str, optional): The name of the target group.
            members (list, optional):
                The members of the target group.  FQDNs, CIDRs, IPRanges, and
                individual IPs are supported.  NOTE: modifying the member list
                is atomic and not additive.  All previous members that are
                desired to be kept within the member list much also be included.
            acls (list, optional):
                A list of ACLs defining how the asset list can be used.  For
                further information on how the ACL dictionaries should be
                written, please refer to the API documentation.  NOTE: modifying
                ACLs is atomic and not additive.  Please provide the complete
                list of ACLs that this asset group will need.
            type (str, optional):
                The type of target group to create.  Valid types are `user` and
                `system`.

        Returns:
            None: The target group has been successfully modified.
        '''
        payload = dict()

        if 'name' in kw:
            payload['name'] = self._check('name', kw['name'], str)
        if 'acls' in kw:
            payload['acls'] = self._check('acls', kw['acls'], list)
        if 'type' in kw:
            payload['type'] = self._check('type', kw['type'], str,
                choices=['system', 'user'])
        if 'members' in kw and len(kw['members']) > 0:
            payload['members'] = ','.join(self._check('members', kw['members'], list))

        # We need to get the current asset group and then merge in the modified
        # data.  We will store the information in the same variable as the
        # modified information was built into.
        for agroup in self.list():
            if agroup['id'] == self._check('id', id, int):
                craw = agroup
        current = {
            'name': craw['name'],
            'acls': craw['acls'],
            'type': craw['type'],
            'members': craw['members'],
        }
        payload = dict_merge(current, payload)

        return self._api.put('target-groups/{}'.format(id), json=payload).json()  

    def list(self):
        '''
        target-groups: list <https://cloud.tenable.com/api#/resources/target-groups/list>`_

        Returns:
            list: Listing of target group resource records.
        '''
        return self._api.get('target-groups').json()['target_groups']               