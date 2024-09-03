from tenable.base.graphql import GraphQLIterator


class CloudSecurityVulnIterator(GraphQLIterator):
    pidx: int = 0
    sidx: int = 0
    vidx: int = 0

    def _increment_counters(self):
        self.count += 1
        self.page_count += 1
        vlen = len(self.page[self.pidx]['Software'][self.sidx]['Vulnerabilities'])
        slen = len(self.page[self.pidx]['Software'])

        self.vidx += 1
        if self.vidx >= vlen:
            self.vidx = 0
            self.sidx += 1
        if self.sidx >= slen:
            self.sidx = 0
            self.pidx += 1

    def _get_next_item(self):
        asset = self.page[self.pidx]
        software = asset['Software'][self.sidx]
        vulnerability = software['Vulnerabilities'][self.vidx]
        return {
            'Asset': {k: v for k, v in asset.items() if k != 'Software'},
            'Software': {k: v for k, v in software.items() if k != 'Vulnerabilities'},
            'Vulnerability': vulnerability
        }
