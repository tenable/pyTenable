'''
'''
from tenable.base.endpoint import APIEndpoint
from .schemas.paging import PaginationSchema
from .schemas.iterators import OTv1Iterator
from box import BoxList


class AssetsAPI(APIEndpoint):
    _path = 'assets'

    def list(self, **kwargs):
        schema = PaginationSchema()
        kwargs['model'] = 'assets'
        return OTv1Iterator(self._api,
            path=self._path,
            payload=schema.load(kwargs)
        )

    def details(self, id):
        return self._get(id)

    def connections(self, id):
        return self._get('{}/connections'.format(id), box=BoxList)