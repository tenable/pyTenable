from .base import CSEndpoint
from tenable.errors import InvalidInputError

class ComplianceAPI(CSEndpoint):
    def status(self, id=None, name=None, repo=None, tag=None):
        '''
        `container-security-policy: policy-compliance-by-id <https://cloud.tenable.com/api#/resources/container-security-policy/policy-compliance-by-id>`_
        `container-security-policy: policy-compliance-by-name <https://cloud.tenable.com/api#/resources/container-security-policy/policy-compliance-by-name>`_

        Either the id or name must be specified.

        Args:
            id (int, optional): The id of the image to query.
            name (str, optional): The name of the image to query.
            repo (str, optional): 
                Only used when specifying by name, it overrides the default
                setting of `library`.
            tag (str, optional):
                Only used when specifying by name, it overrides the default
                setting of `latest`.

        Returns:
            dict: The compliance status of the image querired.
        '''
        # It made logical sense to combine both of these calls together as they
        # are performing the same action, just asking for different peices of
        # information.

        if id:
            return self._api.get('v1/policycompliance', params={
                'image_id': self._check('id', id, str)}).json()
        elif name:
            return self._api.get('v1/compliancebyname', params={
                'image': self._check('name', name, str),
                'repo': self._check('repo', repo, str, default='library'),
                'tag': self._check('tag', tag, str, default='latest')
            }).json()
        else:
            raise InvalidInputError('none of the required options specified')