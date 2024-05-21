"""
test plugins
"""
import uuid

import pytest
import responses

from tenable.ot.graphql.iterators import OTGraphIterator
from tenable.ot.graphql.schema.plugins import Plugin
from tenable.ot.schema.base import AssetInfo, AssetInfoList
from tenable.ot.schema.plugins import PluginDetails, PluginRef


@responses.activate
def test_list(fixture_ot):
    """
    Tests the plugins Graphql list iterator
    """
    responses.add(
        method="POST",
        url="https://localhost/graphql",
        json={
            "data": {
                "plugins": {
                    "pageInfo": {"endCursor": "YXJyYXljb25uZWN0aW9uOjA="},
                    "nodes": [
                        {
                            "id": 720250,
                            "name": "Schneider Electric Modicon Multiple Controllers Unusual or Exceptional Conditions Improper Check",
                            "source": "NNM",
                            "family": "SCADA",
                            "severity": "Medium",
                            "vprScore": None,
                            "comment": None,
                            "owner": None,
                            "totalAffectedAssets": 2,
                            "details": {
                                "id": 720250,
                                "name": "Schneider Electric Modicon Multiple Controllers Unusual or Exceptional Conditions Improper Check",
                                "source": "NNM",
                                "family": "SCADA",
                                "description": "An Improper Check for Unusual or Exceptional Conditions vulnerability exists in the embedded web servers in all Modicon M340, Premium, Quantum PLCs and BMXNOR0200 where an unauthenticated user can send a specially crafted XML data via a POST request to cause the web server to become unavailable.",
                                "solution": "Perform vendor recommended mitigations and apply available vendor upgrades.",
                                "seeAlso": [
                                    "https://www.schneider-electric.com/en/download/document/SEVD-2018-327-01"
                                ],
                                "pluginType": None,
                                "pluginPubDate": None,
                                "pluginModDate": None,
                                "vulnPubDate": None,
                                "vulnModDate": None,
                                "refs": [
                                    {
                                        "name": "CVE",
                                        "value": "CVE-2018-7833",
                                        "url": "http://web.nvd.nist.gov/view/vuln/detail?vulnId=",
                                    }
                                ],
                                "cpe": None,
                                "cvssVector": "CVSS2#AV:N/AC:L/Au:N/C:N/I:N/A:P",
                                "cvssV3Vector": "CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H",
                                "cvssBaseScore": "5.0",
                                "cvssV3BaseScore": "7.5",
                                "cvssV3TemporalScore": "6.5",
                                "cvssTemporalScore": "3.7",
                                "cvssV3TemporalVector": "CVSS:3.0/E:U/RL:O/RC:C",
                                "cvssImpactScore": None,
                            },
                            "affectedAssets": {
                                "nodes": [
                                    {
                                        "id": "d6c19fcd-29ae-441f-bd10-29ab6f9e32e8",
                                        "name": "140-NOE-771-01 Module",
                                    },
                                    {
                                        "id": "e2063853-b284-428a-8205-1c7bdf5afa56",
                                        "name": "BMX NOC0401",
                                    },
                                ]
                            },
                        }
                    ],
                }
            }
        },
    )

    expected = Plugin(
        comment=None,
        family="SCADA",
        id=720250,
        name="Schneider Electric Modicon Multiple Controllers Unusual or "
             "Exceptional Conditions Improper Check",
        owner=None,
        source="NNM",
        severity="Medium",
        total_affected_assets=2,
        vpr_score=None,
        details=PluginDetails(
            id=720250,
            name="Schneider Electric Modicon Multiple "
                 "Controllers Unusual or Exceptional "
                 "Conditions Improper Check",
            source="NNM",
            family="SCADA",
            description="An Improper Check for Unusual or "
                        "Exceptional Conditions "
                        "vulnerability exists in the "
                        "embedded web servers in all Modicon "
                        "M340, Premium, Quantum PLCs and "
                        "BMXNOR0200 where an unauthenticated "
                        "user can send a specially crafted "
                        "XML data via a POST request to "
                        "cause the web server to become "
                        "unavailable.",
            solution="Perform vendor recommended mitigations "
                     "and apply available vendor upgrades.",
            see_also=[
                "https://www.schneider-electric.com/en/download/document/SEVD-2018-327-01"
            ],
            plugin_type=None,
            plugin_pub_date=None,
            plugin_mod_date=None,
            vuln_pub_date=None,
            vuln_mod_date=None,
            refs=[
                PluginRef(
                    name="CVE",
                    value="CVE-2018-7833",
                    url="http://web.nvd.nist.gov/view/vuln/detail?vulnId=",
                )
            ],
            cpe=None,
            cvss_vector="CVSS2#AV:N/AC:L/Au:N/C:N/I:N/A:P",
            cvss_v3_vector="CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H",
            cvss_base_score="5.0",
            cvss_v3_basescore="7.5",
            cvss_v3_temporal_score="6.5",
            cvss_temporal_score="3.7",
            cvss_v3_temporal_vector="CVSS:3.0/E:U/RL:O/RC:C",
            cvss_impact_score=None,
        ),
        affected_assets=AssetInfoList(
            nodes=[
                AssetInfo(
                    id=uuid.UUID("d6c19fcd-29ae-441f-bd10-29ab6f9e32e8"),
                    name="140-NOE-771-01 " "Module",
                ),
                AssetInfo(
                    id=uuid.UUID("e2063853-b284-428a-8205-1c7bdf5afa56"),
                    name="BMX NOC0401",
                ),
            ]
        ),
    )

    resp = fixture_ot.plugins.list()
    assert resp.next() == expected


@responses.activate
def test_plugin(fixture_ot):
    """
    Tests the plugins Graphql plugin retriever
    """
    responses.add(
        method="POST",
        url="https://localhost/graphql",
        json={
            "data": {
                "plugins": {
                    "pageInfo": {"endCursor": "YXJyYXljb25uZWN0aW9uOjA="},
                    "nodes": [
                        {
                            "id": 720250,
                            "name": "Schneider Electric Modicon Multiple Controllers Unusual or Exceptional Conditions Improper Check",
                            "source": "NNM",
                            "family": "SCADA",
                            "severity": "Medium",
                            "vprScore": None,
                            "comment": None,
                            "owner": None,
                            "totalAffectedAssets": 2,
                            "details": {
                                "id": 720250,
                                "name": "Schneider Electric Modicon Multiple Controllers Unusual or Exceptional Conditions Improper Check",
                                "source": "NNM",
                                "family": "SCADA",
                                "description": "An Improper Check for Unusual or Exceptional Conditions vulnerability exists in the embedded web servers in all Modicon M340, Premium, Quantum PLCs and BMXNOR0200 where an unauthenticated user can send a specially crafted XML data via a POST request to cause the web server to become unavailable.",
                                "solution": "Perform vendor recommended mitigations and apply available vendor upgrades.",
                                "seeAlso": [
                                    "https://www.schneider-electric.com/en/download/document/SEVD-2018-327-01"
                                ],
                                "pluginType": None,
                                "pluginPubDate": None,
                                "pluginModDate": None,
                                "vulnPubDate": None,
                                "vulnModDate": None,
                                "refs": [
                                    {
                                        "name": "CVE",
                                        "value": "CVE-2018-7833",
                                        "url": "http://web.nvd.nist.gov/view/vuln/detail?vulnId=",
                                    }
                                ],
                                "cpe": None,
                                "cvssVector": "CVSS2#AV:N/AC:L/Au:N/C:N/I:N/A:P",
                                "cvssV3Vector": "CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H",
                                "cvssBaseScore": "5.0",
                                "cvssV3BaseScore": "7.5",
                                "cvssV3TemporalScore": "6.5",
                                "cvssTemporalScore": "3.7",
                                "cvssV3TemporalVector": "CVSS:3.0/E:U/RL:O/RC:C",
                                "cvssImpactScore": None,
                            },
                            "affectedAssets": {
                                "nodes": [
                                    {
                                        "id": "d6c19fcd-29ae-441f-bd10-29ab6f9e32e8",
                                        "name": "140-NOE-771-01 Module",
                                    },
                                    {
                                        "id": "e2063853-b284-428a-8205-1c7bdf5afa56",
                                        "name": "BMX NOC0401",
                                    },
                                ]
                            },
                        }
                    ],
                }
            }
        },
    )

    expected = Plugin(
        comment=None,
        family="SCADA",
        id=720250,
        name="Schneider Electric Modicon Multiple Controllers Unusual or "
             "Exceptional Conditions Improper Check",
        owner=None,
        source="NNM",
        severity="Medium",
        total_affected_assets=2,
        vpr_score=None,
        details=PluginDetails(
            id=720250,
            name="Schneider Electric Modicon Multiple "
                 "Controllers Unusual or Exceptional "
                 "Conditions Improper Check",
            source="NNM",
            family="SCADA",
            description="An Improper Check for Unusual or "
                        "Exceptional Conditions "
                        "vulnerability exists in the "
                        "embedded web servers in all Modicon "
                        "M340, Premium, Quantum PLCs and "
                        "BMXNOR0200 where an unauthenticated "
                        "user can send a specially crafted "
                        "XML data via a POST request to "
                        "cause the web server to become "
                        "unavailable.",
            solution="Perform vendor recommended mitigations "
                     "and apply available vendor upgrades.",
            see_also=[
                "https://www.schneider-electric.com/en/download/document/SEVD-2018-327-01"
            ],
            plugin_type=None,
            plugin_pub_date=None,
            plugin_mod_date=None,
            vuln_pub_date=None,
            vuln_mod_date=None,
            refs=[
                PluginRef(
                    name="CVE",
                    value="CVE-2018-7833",
                    url="http://web.nvd.nist.gov/view/vuln/detail?vulnId=",
                )
            ],
            cpe=None,
            cvss_vector="CVSS2#AV:N/AC:L/Au:N/C:N/I:N/A:P",
            cvss_v3_vector="CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H",
            cvss_base_score="5.0",
            cvss_v3_basescore="7.5",
            cvss_v3_temporal_score="6.5",
            cvss_temporal_score="3.7",
            cvss_v3_temporal_vector="CVSS:3.0/E:U/RL:O/RC:C",
            cvss_impact_score=None,
        ),
        affected_assets=AssetInfoList(
            nodes=[
                AssetInfo(
                    id=uuid.UUID("d6c19fcd-29ae-441f-bd10-29ab6f9e32e8"),
                    name="140-NOE-771-01 " "Module",
                ),
                AssetInfo(
                    id=uuid.UUID("e2063853-b284-428a-8205-1c7bdf5afa56"),
                    name="BMX NOC0401",
                ),
            ]
        ),
    )

    resp = fixture_ot.plugins.plugin(720250)
    plugin = resp.next()
    affected_assets = iter(plugin.affected_assets)
    assert len(list(affected_assets)) == 2
    assert plugin == expected


@pytest.mark.vcr()
def test_plugins_list_vcr(api):
    """
    Tests the assets Graphql list iterator with cassettes
    """
    plugins = api.plugins.list(limit=2)
    assert isinstance(plugins, OTGraphIterator)
    plugin = plugins.next()
    assert plugin is not None
