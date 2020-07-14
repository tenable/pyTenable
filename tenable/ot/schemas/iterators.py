from restfly.iterator import APIIterator
from box import BoxList
from copy import copy


class OTIterator(APIIterator):
    _path = None
    limit = 500
    offset = 0

    def __init__(self, api, **kwargs):
        self._path = kwargs.pop('path')
        self._payload = kwargs.pop('payload')
        self.limit = kwargs.get('limit', self.limit)
        self.offset = kwargs.get('offset', self.offset)
        super(OTIterator, self).__init__(api, **kwargs)

    def _get_page(self):
        p = copy(self._payload)
        p['offset'] = self.offset
        p['limit'] = self.limit
        self.page = self._api.post(self._path, json=p, box=BoxList)
        self.offset += self.limit