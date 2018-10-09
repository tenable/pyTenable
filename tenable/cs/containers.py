from .base import CSEndpoint

class ContainersAPI(CSEndpoint):
    def list(self):
        '''
        `container-security-containers: list-containers <https://cloud.tenable.com/api#/resources/container-security-containers/list-containers>`_

        Returns:
            list: List of container resource records
        '''
        return self._api.get('v1/container/list').json()

    def inventory(self, id):
        '''
        `container-security-containers: image-inventory <https://cloud.tenable.com/api#/resources/container-security-containers/image-inventory>`_

        Args:
            id (str): The image identifier

        Returns:
            dict: The image inventory
        '''
        return self._api.get('v1/container/{}/status'.format(
            self._check('id', id, str))).json()