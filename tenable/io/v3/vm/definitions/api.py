from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint


class VMDefinitionsAPI(ExploreBaseEndpoint):

    def agent_config(self):
        raise NotImplementedError()
