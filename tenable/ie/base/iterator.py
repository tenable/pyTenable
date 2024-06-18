from restfly import APIIterator


class ADIterator(APIIterator):
    '''
    The following methods allows us to iterate through pages and get data

    Attributes:
        _api (restfly.session.APISession):
            The APISession object that will be used for querying for the
            data.
        _path (str):
            The URL for API call.
        _schema (object):
            The marshmallow schema object for deserialized response.
        _method (str):
            The API request method. supported values are ``get`` and ``post``.
            default is ``get``
        _query (dict):
            The query params for API call.
        _payload (dict):
            The payload object for API call. it is applicable only for
            post method.
    '''
    _api = None
    _query = None
    _payload = None
    _method = None
    _per_page = None
    _path = None
    _schema = None

    def _get_page(self) -> None:
        '''
        Request the next page of data
        '''
        # The first thing that we need to do is construct the query with the
        # current page and per_page
        query = self._query
        query['page'] = self.num_pages
        query['perPage'] = self._per_page

        # Lets make the actual call at this point.
        if self._method == 'post':
            self.page = self._schema.load(
                self._api.post(self._path, params=query, json=self._payload),
                many=True)
        else:
            self.page = self._schema.load(
                self._api.get(self._path, params=query),
                many=True)
