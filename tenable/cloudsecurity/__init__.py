from typing import Dict
from pathlib import Path
from tenable.base.graphql import GraphQLSession

from .assets.api import AssetsAPI
from .vulns.api import VulnsAPI


class CloudSecurity(GraphQLSession):
    _query_folder: Path = Path(__file__).parent.joinpath('queries')
    _base_path: str = 'api/graph'
    _env_base: str = 'TCS'

    def _authorization(self, api_key: str) -> Dict:
        return {
            'Authorization': f'Bearer {api_key}'
        }

    @property
    def assets(self):
        return AssetsAPI(self)

    @property
    def vulns(self):
        return VulnsAPI(self)
