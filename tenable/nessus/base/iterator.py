from copy import copy
from restfly.iterator import APIIterator


class PaginationIterator(APIIterator):
    limit: int = 1000
    offset: int = 0
    query: dict = {}
    path: str = None
    envelope: str = None

    def _get_page(self):
        query = copy(self.query)
        query['limit'] = self.limit
        query['offset'] = self.offset
        resp = self._api.get(self.path, params=query)
        self.page = resp[self.envelope]
        self.offset += self.limit
