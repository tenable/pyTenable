'''
'''
from tenable.base.endpoint import APIEndpoint
from .schemas.paging import PaginationSchema
from .schemas.iterators import OTv1Iterator


class NetworkInterfacesAPI(APIEndpoint):
    _path = 'networkinterfaces'

    def details(self, id):
        return self._get(id)

    def connections(self, id):
        return self._get('{}/connections'.format(id))