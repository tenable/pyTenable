'''
Vulnerabilities
===============

Methods described in this section relate to the the vulnerabilities API.
These methods can be accessed at ``TenableOT.vulns``.

.. rst-class:: hide-signature
.. autoclass:: VulnsAPI
    :members:

.. autoclass:: VulnAssetIntermixer
    :members:
'''
from tenable.base.endpoint import APIEndpoint
from .schemas.paging import PaginationSchema
from .schemas.iterators import OTIterator
from box import Box, BoxList
from copy import copy


class VulnAssetIntermixer(object):
    '''
    This iterator will make the appropriate calls to construct a "vulnerability
    instance" similar to the Tenable.io vuln export APIs and the Tenable.sc
    analysis APIs.

    .. note::
        This iterator should not be instantiated on your own.  It relies on
        parameters passed from :py:meth:`tenable.ot.vulns.VulnsAPI.export`.

    Example:
        >>> vulns = ot.vulns.extract()
        >>> for vuln in vulns:
        ...     print(vuln)
    '''
    _asset_cache = dict()
    _va_iterator = None
    _vulns = None
    _vulns_idx = 0
    count = 0
    asset_count = 0
    vuln_count = 0

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def __init__(self, api):
        self._api = api

    def _merge_cache(self, asset):
        '''
        Returns a "vuln instance" of a merged asset, vuln def, and connections.
        '''
        if asset['id'] not in self._asset_cache:
            connections = self._api.assets.connections(asset['id'])
            for con in connections:
                iface = self._api.network_interfaces.details(con['networkInterface'])
                iface['id'] = con['networkInterface']
                con['networkInterface'] = iface
            self._asset_cache[asset['id']] = connections
            self.asset_count += 1
        asset.connections = self._asset_cache[asset.id]
        vuln = copy(self._vulns[self._vulns_idx])
        vuln['asset'] = asset
        vuln['cve']['id'] = vuln['cve']['CVE_data_meta']['ID']
        return Box(vuln, box_attrs=self._api._box_attrs)

    def _get_next_vai(self):
        '''
        Gets the next Vulnerability Asset Iterator
        '''
        self._va_iterator = self._api.vulns.vuln_assets(
            self._vulns[self._vulns_idx]['cve']['CVE_data_meta']['ID']
        )
        self.vuln_count += 1

    def next(self):
        '''
        Retrieves the next item.

        .. note::
            The next method of the iterator is called automatically when using
            the iterator as an iterable (for example within a for loop).  Using
            next manually should only be used when you want to advance the
            iterator on your own.

        Returns:
            :obj:`dict`:
                The next vulnerability instance item.
        '''
        if not self._vulns:
            self._vulns = self._api.vulns.list(box=False).json()

        if not self._va_iterator:
            self._get_next_vai()

        resp = None
        while not resp:
            try:
                resp = self._merge_cache(self._va_iterator.next())
                self.count += 1
            except StopIteration:
                self._vulns_idx += 1
                try:
                    self._get_next_vai()
                except IndexError:
                    raise StopIteration
        return resp


class VulnsAPI(APIEndpoint):
    _path = 'vulnerabilities'

    def list(self, **kwargs):
        '''
        Returns a list of vulnerability definitions.

        Returns:
            :obj:`list`:
                The list of vulnerability definitions.

        Example:
            >>> vulns = ot.vulns.list()
        '''
        box = kwargs.pop('box', BoxList)
        return self._get(params=kwargs, box=box)

    def assets_list(self):
        '''
        Returns a summarization showing the count of assets that have each
        vulnerability definition.

        Returns:
            :obj:`list`:
                The list of vulnerability definition asset summaries.

        Example:
            >>> summaries = ot.vulns.assets_list()
        '''
        return self._get('assets', box=BoxList)

    def vuln_assets(self, id, **kwargs):
        '''
        Retrieves the list of assets that have a given vulnerability
        definition.

        Args:
            id (str):
                The unique identifier for the vuln definition.

        Returns:
            :obj:`OTIterator`:
                An iterator object that will handle pagination of the data.

        Example:
            >>> for asset in ot.vulns.vuln_assets(id):
            ...     print(asset)
        '''
        schema = PaginationSchema()
        return OTIterator(self._api,
            path='{}/{}/assets'.format(self._path, id),
            payload=schema.load(kwargs)
        )

    def extract(self):
        '''
        Returns an iterator that handles blending the vulnerability definition
        data and asset data into a "vulnerability instance" as is commonly seen
        in Tenable.io and Tenable.sc

        Returns:
            :obj:`VulnAssetIntermixer`:
                The iterator object handling the data blending.

        Example:
            >>> for vuln in ot.vulns.extract():
            ...     print(vuln)
        '''
        return VulnAssetIntermixer(self._api)