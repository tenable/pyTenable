from .base import CSEndpoint

class ImportAPI(CSEndpoint):
    def _gen_import_payload(self, kw):
        '''
        As the post to create and update use the same options, we have pulled
        the option checking into this function to handle validation.
        '''

        # Required parameters
        payload = {
            'host': self._check('host', kw['host'], str),
            'port': self._check('port', kw['port'], int),
            'username': self._check('username', kw['username'], str),
            'password': self._check('password', kw['password'], str),
            'provider': self._check('provider', kw['provider'], str, choices=[
                'dr',   # Docker Registry
                'dre',  # Docker Enterprise Edition Registry
                'ecr',  # Amazon ECR
                'jfa',  # jFrog Artifactory
            ]),
            'ssl': self._check('ssl', kw['ssl'], bool) if 'ssl' in kw and kw['ssl'] != None else True,
        }

        # return the completed payload
        return payload

    def list(self):
        '''
        `container-security-import: list-imports <https://cloud.tenable.com/api#/resources/container-security-import/list-imports>`_

        Returns:
            list: List of all import resource records
        '''
        return self._api.get('v1/import/list').json()

    def test(self, id):
        '''
        `container-security-import: test-connection <https://cloud.tenable.com/api#/resources/container-security-import/test-connection>`_

        Args:
            id (int): A test id for the purposes of testing the connection.

        Returns:
            dict: The response with the status and id.
        '''
        self._api.get('v1/import/{}/test'.format(
            self._check('id', id, 'uuid'))).json()

    def create(self, **kw):
        '''
        `container-security-import: import <https://cloud.tenable.com/api#/resources/container-security-import/import>`_

        Args:
            host (str): The address for the registry to import from.
            port (int): The port number that the registry resides on.
            username (str): The username to authenticate to the registry with.
            password (str): The password to authenticate to the registry with.
            provider (str): The registry provider to use.
            ssl (bool): Is SSL used for communication?  Default is True.

        Returns:
            dict: The id and status of the specified request.
        '''
        payload = self._gen_import_payload(kw)
        return self._api.post('v1/import', json=payload).json()

    def update(self, id, **kw):
        '''
        `container-security-import: update-import-by-id <https://cloud.tenable.com/api#/resources/container-security-import/update-import-by-id>`_

        Args:
            id (int): The import job identifier.
            host (str): The address for the registry to import from.
            port (int): The port number that the registry resides on.
            username (str): The username to authenticate to the registry with.
            password (str): The password to authenticate to the registry with.
            provider (str): The registry provider to use.
            ssl (bool): Is SSL used for communication?  Default is True.

        Returns:
            dict: The id and status of the specified request.
        '''
        payload = self._gen_import_payload(kw)
        return self._api.post('v1/import/{}'.format(
            self._check('id', id, 'uuid')), json=payload).json()

    def delete(self, id):
        '''
        `container-security-import: delete-import-by-id <https://cloud.tenable.com/api#/resources/container-security-import/delete-import-by-id>`_

        Args:
            id (int): The unique identifier of the import job to delete.

        Returns:
            dict: Returns the status and id of the deleted import.
        '''
        return self._api.delete('v1/import/{}'.format(self._check('id', id, 'uuid'))).json()

    def run(self, id):
        '''
        `container-security-import: run-import-by-id <https://cloud.tenable.com/api#/resources/container-security-import/run-import-by-id>`_

        Args:
            id (int): The unique identifier of the import job to run.

        Returns:
            dict: Returns the status and id of the run import.
        '''
        return self._api.post('v1/import/{}/run'.format(self._check('id', id, 'uuid')), json={}).json()

      