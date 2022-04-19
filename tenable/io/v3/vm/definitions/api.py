'''
VM Definitions
==============

The following methods allow for interaction into the Tenable.io
:devportal:`definitions <definitions>` API endpoints.

Methods available on ``tio.v3.vm.definitions``:

.. rst-class:: hide-signature
.. autoclass:: VMDefinitionsAPI
    :members:
'''
from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint


class VMDefinitionsAPI(ExploreBaseEndpoint):

    _conv_json = True

    def agent_exclusions(self):
        return self._get('api/v3/definitions/agent-exclusions')

    def agent_groups(self):
        return self._get('api/v3/definitions/agent-groups')

    def agents(self):
        return self._get('api/v3/definitions/agents')

    def assets(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')

    def audit_logs(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')

    def credentials(self):
        return self._get('api/v3/definitions/credentials')

    def editors(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')

    def exclusions(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')

    def folders(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')

    def networks(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')

    def plugin_families(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')

    def plugins(self):
        return self._get('api/v3/definitions/plugins')

    def policies(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')

    def remediation_scans(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')

    def scanner_groups(self):
        return self._get('api/v3/definitions/scanner-groups')

    def scanners(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')

    def scans(self):
        return self._get('api/v3/definitions/scans')

    def tag_categories(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')

    def tags(self):
        return self._get('api/v3/definitions/tags/assets/')

    def vulnerabilities(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')
