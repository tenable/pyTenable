from typing import Dict
from pathlib import Path
from tenable.base.graphql import GraphQLSession


class CloudSecurity(GraphQLSession):
    _query_folder: Path = Path(__file__).parent.joinpath('queries')
    _base_path: str = 'api/graph'
    _env_base: str = 'TCS'

    def _authorization(self, api_key: str) -> Dict:
        return {
            'Authorization': f'Bearer {api_key}'
        }
