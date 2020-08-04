from restfly.iterator import APIIterator
from box import BoxList
from copy import copy


class OTIterator(APIIterator):
    _path = None
    limit = 500
    offset = 0

    def __init__(self, api, **kwargs):
        self._path = kwargs.pop('path')
        self._payload = kwargs.pop('payload', {})
        self.limit = kwargs.get('limit', self.limit)
        self.offset = kwargs.get('offset', self.offset)
        super(OTIterator, self).__init__(api, **kwargs)

    def _get_page(self):
        '''
        Retrieves the next page of data
        '''
        # if the size of the page is less than the limit, then we will simply
        # bail and let iterator stop.
        if self.num_pages > 0 and len(self.page) < self.limit:
            raise StopIteration()

        # make a copy of the payload (so not to pollute it) and then set the
        # offset and limits.
        p = copy(self._payload)
        p['offset'] = self.offset
        p['limit'] = self.limit

        # make the call and update the offset.
        self.page = self._api.post(self._path, json=p, box=BoxList)
        self.offset += self.limit