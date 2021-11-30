'''
Container Security Iterator module.
'''
from restfly.iterator import APIIterator


class CSIterator(APIIterator):
    '''
    Container Security API Iterator
    '''
    _path: str
    _params: dict
    _limit: int = 0
    _offset: int = 1000

    def _get_page(self):
        self._params['limit'] = self._limit
        self._params['offset'] = self._offset
        resp = self._api.get(self._path, params=self._params, conv_json=True)
        self._offset += self._limit
        self.total = resp['pagination']['total']
        self.page = resp['items']
