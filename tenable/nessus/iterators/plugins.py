from typing import Dict, List
from copy import copy
from restfly.iterator import APIIterator


class PluginIterator(APIIterator):
    plugins: List[int] = []
    plugin_idx: int = 0
    total: int = None

    def __init__(self, api, **kw):
        super().__init__(api, **kw)
        for fam in self._api.plugins.families():
            family = self._api.plugins.family_details(fam['id'])
            self.plugins += [p['id'] for p in family['plugins']]
        self.total = len(self.plugins)

    def __getitem__(self, idx: int) -> Dict:
        return self._api.plugins.plugin_details(self.plugins[idx])

    def next(self):
        if self.plugin_idx >= self.total:
            raise StopIteration()
        self.plugin_idx += 1
        return self[self.plugin_idx - 1]
