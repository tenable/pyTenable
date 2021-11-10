'''
test assets
'''
import responses
from tenable.ot.graphql.assets import (
    Asset,
    Risk,
    Segment
)


@responses.activate
def test_list(fixture_ot):
    '''
    Tests the assets Graphql list iterator
    '''
    responses.add(
        method='POST',
        url='https://localhost/graphql',
        json={
            "data": {
                "assets": {
                    "pageInfo": {
                        "endCursor": "YXJyYXljb25uZWN0aW9uOjA="
                    },
                    "nodes": [
                        {
                            "id": "ff950a25-2955-457a-9168-84374ee97f23",
                            "slot": None,
                            "name": "Dummy network device",
                            "type": "NetworkDevice",
                            "risk": {
                                "unresolvedEvents": 0,
                                "totalRisk": 0
                            },
                            "criticality": "MediumCriticality",
                            "ips": {
                                "nodes": []
                            },
                            "macs": {
                                "nodes": [
                                    "5c:88:16:01:9f:80"
                                ]
                            },
                            "category": "NetworkAssetsCategory",
                            "vendor": "Rockwell",
                            "family": None,
                            "model": None,
                            "firmwareVersion": None,
                            "os": None,
                            "runStatus": None,
                            "purdueLevel": "Level2",
                            "firstSeen": "2021-09-11T22:24:38.70483Z",
                            "lastSeen": "2021-09-11T22:24:38.663888Z",
                            "location": None,
                            "backplane": None,
                            "description": "Dummy description",
                            "segments": {
                                "nodes": [
                                    {
                                        "id": "4629be3c-c59b-482d-a61a-77079c4b7861",
                                        "name": "NetworkDevice / No Ip",
                                        "type": "Segment",
                                        "key": "AG1-6",
                                        "systemName": "NetworkDevice / No Ip",
                                        "vlan": None,
                                        "description": None,
                                        "assetType": "NetworkDevice",
                                        "subnet": "No Ip"
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        }
    )

    expected = Asset(
        id="ff950a25-2955-457a-9168-84374ee97f23",
        name="Dummy network device",
        type="NetworkDevice",
        risk=Risk(
            unresolved_events=0,
            total_risk=0
        ),
        criticality="MediumCriticality",
        category="NetworkAssetsCategory",
        purdue_level="Level2",
        ips=[],
        macs=["5c:88:16:01:9f:80"],
        vendor="Rockwell",
        first_seen="2021-09-11T22:24:38.70483Z",
        last_seen="2021-09-11T22:24:38.663888Z",
        description="Dummy description",
        segments=[
            Segment(
                id="4629be3c-c59b-482d-a61a-77079c4b7861",
                name="NetworkDevice / No Ip",
                type="Segment",
                key="AG1-6",
                system_name="NetworkDevice / No Ip",
                asset_type="NetworkDevice",
                subnet="No Ip"
            )
        ]
    )

    resp = fixture_ot.assets.list()
    assert resp.next() == expected

