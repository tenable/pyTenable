from typing import Dict
from restfly.iterator import APIIterator


class OTExportsIterator(APIIterator):
    """
    Tenable OT Security Exports Iterator
    """
    _model: str
    _query: str
    _variables: Dict

    def _get_page(self):
        """
        Fetches the next page of data from the GraphQL API
        """
        resp = self._api.graphql(query=self._query,
                                 variables=self._variables,
                                 )
        raw_page = resp.get('data', {}).get(self._model, {})
        self.page = raw_page.get('nodes', [])
        self._variables['startAt'] = raw_page.get('pageInfo', {})\
                                             .get('endCursor', None)
        self.total = raw_page.get('count')
        return self.page


class OTFindingsIterator(APIIterator):
    """
    Tenable OT Security Findings Iterator
    """
    empty_asset_count: int = 0
    _assets: OTExportsIterator

    def _get_page(self):
        """
        Fetches the next page of findings from the
        v1 REST API.
        """
        items = []
        counter = -1
        while len(items) == 0:
            counter += 1
            try:
                asset = self._assets.next()
            except StopIteration:
                raise StopIteration()
            self._asset_id = asset['id']
            items = self._api.get(f'v1/assets/{self._asset_id}/plugin_hits')
        self.page = items
        self.empty_asset_count += counter
        return self.page
