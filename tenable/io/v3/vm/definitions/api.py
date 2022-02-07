from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint


class VMDefinitionsAPI(ExploreBaseEndpoint):

    def agent_exclusions(self):
        return self._get('api/v3/definitions/agent-exclusions')

    def agent_groups(self):
        return self._get('api/v3/definitions/agent-groups')

    def agents(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')

    def assets(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')

    def audit_logs(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')

    def credentials(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')

    def editors(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')

    def exclusions(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')

    def folders(self):
        return self._get('api/v3/definitions/folders')

    def networks(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')

    def plugin_families(self):
        return self._get('api/v3/definitions/plugin_families')

    def plugins(self):
        return self._get('api/v3/definitions/plugins')

    def policies(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')

    def remediation_scans(self):
        return self._get('api/v3/definitions/groups')

    def scanner_groups(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')

    def scanners(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')

    def scans(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')

    def tag_categories(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')

    def tags(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')

    def vulnerabilities(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')
