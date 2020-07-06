'''
'''
from tenable.base.endpoint import APIEndpoint
from .schemas.paging import PaginationSchema
from .schemas.iterators import OTv1Iterator
from box import Box, BoxList
from copy import copy


class VulnAssetIntermixer(object):
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
        if asset.id not in self._asset_cache:
            connections = self._api.assets.connections(asset.id)
            for con in connections:
                iface = self._api.network_interfaces.details(con.network_interface)
                iface.id = con.network_interface
                con.network_interface = iface
            self._asset_cache[asset.id] = connections
            self.asset_count += 1
        asset.connections = self._asset_cache[asset.id]
        vuln = copy(self._vulns[self._vulns_idx])
        vuln.asset = asset
        vuln.cve.id = vuln.cve.CVE_data_meta.ID
        return vuln

    def _get_next_vai(self):
        self._va_iterator = self._api.vulns.vuln_assets(
            self._vulns[self._vulns_idx].cve.CVE_data_meta.ID)
        self.vuln_count += 1

    def next(self):
        if not self._vulns:
            self._vulns = self._api.vulns.list()

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
        return self._get(params=kwargs, box=BoxList)

    def assets_list(self):
        return self._get('assets', box=BoxList)

    def vuln_assets(self, id, **kwargs):
        schema = PaginationSchema()
        #kwargs['model'] = 'assets'
        return OTv1Iterator(self._api,
            path='{}/{}/assets'.format(self._path, id),
            payload=schema.load(kwargs)
        )

    def extract(self):
        return VulnAssetIntermixer(self._api)