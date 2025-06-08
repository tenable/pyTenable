import json

import pytest
import responses

from tenable.exposuremanagement.inventory.assets.schema import AssetClass, Assets
from tenable.exposuremanagement.inventory.schema import Field, Properties, SortDirection, QueryMode, PropertyFilter, \
    Operator


@pytest.fixture
def asset_properties_response() -> dict[str, list[dict]]:
    return {"properties": [{"key": "asset_id", "readable_name": "Asset ID",
                            "control": {"type": "STRING", "multiple_allowed": True,
                                        "regex": {"hint": "01234567-abcd-ef01-2345-6789abcdef01",
                                                  "expression": "[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}(,[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12})*"}},
                            "operators": ["=", "!=", "exists", "not exists"], "sortable": True, "filterable": True,
                            "weight": 0.0,
                            "object_types": ["ACCOUNT", "APPLICATION", "CONTAINER", "GENERAL", "DEVICE", "GROUP",
                                             "STORAGE", "RESOURCE", "ROLE"],
                            "description": "# Asset ID\n## A unique identifier for an asset\n\nAn asset ID is a unique identifier that is assigned to each asset in a cyber asset management system. This identifier can be used to track the asset, its associated vulnerabilities, and its security posture. Asset IDs are typically generated automatically by the asset management system, but they can also be manually assigned.\n\nHere are some key points to understand about asset IDs in the context of the cyber industry:\n- **Uniqueness**: Asset IDs must be unique within the asset management system. This ensures that each asset can be easily identified and tracked.\n- **Accuracy**: Asset IDs must be accurate and up-to-date. This ensures that the asset management system has the most accurate information about each asset.\n- **Consistency**: Asset IDs must be consistent across all systems and applications that use them. This ensures that there is no confusion about which asset is being referred to.\n\nAsset IDs are an important part of cyber asset management. They help to track assets, their associated vulnerabilities, and their security posture. Asset IDs must be unique, accurate, and consistent.\n"},
                           {"key": "asset_class", "readable_name": "Asset Class",
                            "control": {"type": "STRING", "multiple_allowed": True,
                                        "selection": [{"name": "Account", "value": "ACCOUNT", "deprecated": False},
                                                      {"name": "Web Application", "value": "APPLICATION",
                                                       "deprecated": False},
                                                      {"name": "Container", "value": "CONTAINER", "deprecated": False},
                                                      {"name": "Other Resource", "value": "GENERAL",
                                                       "deprecated": False},
                                                      {"name": "Device", "value": "DEVICE", "deprecated": False},
                                                      {"name": "Group", "value": "GROUP", "deprecated": False},
                                                      {"name": "Infrastructure As Code", "value": "IAC",
                                                       "deprecated": True},
                                                      {"name": "Storage", "value": "STORAGE", "deprecated": False},
                                                      {"name": "Person", "value": "IDENTITY", "deprecated": True},
                                                      {"name": "Resource", "value": "RESOURCE", "deprecated": False},
                                                      {"name": "Role", "value": "ROLE", "deprecated": False}]},
                            "operators": ["=", "!=", "exists", "not exists"], "sortable": True, "filterable": True,
                            "weight": 0.0,
                            "object_types": ["ACCOUNT", "APPLICATION", "CONTAINER", "GENERAL", "DEVICE", "GROUP",
                                             "STORAGE", "RESOURCE", "ROLE"],
                            "description": "# Asset Class\n## A group of assets that share common characteristics\n\nAn asset class is a group of assets that share common characteristics. For example, all computers in an organization might be considered one asset class, while all servers might be considered another. Asset classes can be used to group assets together for reporting, analysis, and other purposes.\n\nHere are some key points to understand about asset classes in the context of the cyber industry:\n- **Asset Classes and Asset Types**: Asset classes are typically defined based on asset type. For example, all computers might be considered one asset type, while all servers might be considered another.\n- **Asset Classes and Asset Subtypes**: Asset classes can also be defined based on asset subtype. For example, all laptops might be considered one asset subtype, while all desktops might be considered another.\n- **Asset Classes and Asset Groups**: Asset classes can also be used to group assets together into asset groups. For example, all assets that are located in the same building might be considered one asset group, while all assets that are owned by the same department might be considered another.\n\nAsset classes can be a valuable tool for managing and understanding assets. By grouping assets together based on common characteristics, asset classes can make it easier to track assets, identify risks, and make informed decisions about asset management.\n"},
                           {"key": "asset_name", "readable_name": "Asset Name",
                            "control": {"type": "STRING", "multiple_allowed": False,
                                        "regex": {"hint": "hostname", "expression": ".*"}},
                            "operators": ["contains", "not contains", "=", "!=", "exists", "not exists"],
                            "sortable": True, "filterable": True, "weight": 1.0,
                            "object_types": ["ACCOUNT", "APPLICATION", "CONTAINER", "GENERAL", "DEVICE", "GROUP",
                                             "STORAGE", "RESOURCE", "ROLE"],
                            "description": "# Asset Name\n## The name of an asset\n\nThe asset name is a unique identifier for an asset. It is used to track the asset and its associated data. The asset name can be any string of characters, but it is recommended to use a name that is descriptive and easy to remember.\n\nHere are some key points to understand about asset names in the context of the cyber industry:\n- **Asset names should be unique**. This is important to ensure that each asset can be easily identified and tracked.\n- **Asset names should be descriptive**. This will help users to understand what the asset is and what it does.\n- **Asset names should be easy to remember**. This will make it easier for users to find the assets they need.\n\n## Examples of asset names:\n- **Server1**\n- **Router2**\n- **Database3**\n- **Laptop4**\n- **Printer5**\n"},
                           {"key": "sources", "readable_name": "Sources",
                            "control": {"type": "STRING", "multiple_allowed": True,
                                        "selection": [{"name": "AWS Connector", "value": "AWS", "deprecated": True},
                                                      {"name": "AWS SSM agent", "value": "SSM", "deprecated": True},
                                                      {"name": "Agent", "value": "NESSUS_AGENT", "deprecated": True},
                                                      {"name": "Azure Connector", "value": "AZURE", "deprecated": True},
                                                      {"name": "Azure Frictionless Assessment", "value": "AZURE_FA",
                                                       "deprecated": True},
                                                      {"name": "GCP Connector", "value": "GCP", "deprecated": True},
                                                      {"name": "Nessus Network Monitor", "value": "PVS",
                                                       "deprecated": True},
                                                      {"name": "Nessus", "value": "NESSUS_SCAN", "deprecated": True},
                                                      {"name": "Tenable Web Application Scanning", "value": "WAS",
                                                       "deprecated": False},
                                                      {"name": "Tenable Identity Exposure", "value": "TIE",
                                                       "deprecated": False},
                                                      {"name": "Tenable Cloud Security (Legacy)", "value": "T.CS",
                                                       "deprecated": True},
                                                      {"name": "Tenable Cloud Security", "value": "CLOUD",
                                                       "deprecated": False},
                                                      {"name": "Tenable Attack Surface Management", "value": "ASM",
                                                       "deprecated": False},
                                                      {"name": "Tenable Vulnerability Management", "value": "T.IO",
                                                       "deprecated": False},
                                                      {"name": "Tenable OT Security", "value": "T.OT",
                                                       "deprecated": False},
                                                      {"name": "Tenable Container Security", "value": "CONSEC",
                                                       "deprecated": False}, {"name": "Tenable Cloud Security (core)",
                                                                              "value": "CORE_CLOUDRESOURCE",
                                                                              "deprecated": True},
                                                      {"name": "Qualys VMDR", "value": "QUALYS", "deprecated": False,
                                                       "third_party": True},
                                                      {"name": "SentinelOne Singularity", "value": "SENTINEL_ONE",
                                                       "deprecated": False, "third_party": True},
                                                      {"name": "Rapid7 InsightVM", "value": "RAPID_7",
                                                       "deprecated": True},
                                                      {"name": "Tenable Security Center", "value": "SECURITY_CENTER",
                                                       "deprecated": False},
                                                      {"name": "Carbon Black Workload", "value": "CARBON_BLACK",
                                                       "deprecated": True},
                                                      {"name": "Microsoft Defender", "value": "MICROSOFT_DEFENDER",
                                                       "deprecated": False, "third_party": True},
                                                      {"name": "CrowdStrike Falcon", "value": "CROWDSTRIKE",
                                                       "deprecated": False},
                                                      {"name": "ServiceNow", "value": "SERVICE_NOW",
                                                       "deprecated": False},
                                                      {"name": "Unclassified", "value": "UNCLASSIFIED",
                                                       "deprecated": False}]}, "operators": ["=", "!="],
                            "sortable": True,
                            "filterable": True, "weight": 1.0,
                            "object_types": ["ACCOUNT", "APPLICATION", "CONTAINER", "GENERAL", "DEVICE", "GROUP",
                                             "STORAGE",
                                             "RESOURCE", "ROLE"],
                            "description": "# Sources\n## The origin of the data\n\nSources are the origin of the data. They can be internal (e.g., data collected by the organization's own systems) or external (e.g., data purchased from a third-party vendor).\n\nHere are some key points to understand about sources in the context of the cyber industry:\n- **Internal Sources**: These are data collected by the organization's own systems. Examples include data from network devices, servers, endpoints, and applications.\n- **External Sources**: These are data purchased from a third-party vendor. Examples include data from vulnerability databases, threat intelligence feeds, and market research reports.\n\nSources are important because they provide context for the data. They can help to determine the accuracy, reliability, and timeliness of the data. They can also help to identify the potential risks associated with the data.\n"},
                           {"key": "created_at", "readable_name": "Created Date",
                            "control": {"type": "DATE", "multiple_allowed": False,
                                        "regex": {"hint": "timestamp", "expression": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"}},
                            "operators": ["=", ">", "<", "between", "exists", "not exists", "older than", "newer than",
                                          "within last"], "sortable": True, "filterable": True, "weight": 0.0,
                            "object_types": ["ACCOUNT", "APPLICATION", "CONTAINER", "GENERAL", "DEVICE", "GROUP",
                                             "STORAGE", "RESOURCE", "ROLE"],
                            "description": "# Created Date\n## The date and time an asset was created\n\nThe created date is the date and time an asset was first created in the system. This can be useful for tracking the age of assets and identifying those that may be outdated or no longer in use.\n\nHere are some key points to understand about created dates in the context of the cyber industry:\n- **Created dates can be used to track the age of assets**. This can be helpful for identifying assets that may be outdated or no longer in use.\n- **Created dates can also be used to identify assets that have been recently created**. This can be helpful for tracking down new assets that may be vulnerable to attack.\n- **Created dates can be used to identify assets that have been modified**. This can be helpful for tracking changes to assets and identifying potential security risks.\n\nCreated dates are an important part of asset management and can be used for a variety of purposes. By understanding created dates, you can better track the age, status, and security of your assets.\n"},
                           {"key": "first_observed_at", "readable_name": "First Observation Date",
                            "control": {"type": "DATE", "multiple_allowed": False, "regex": {"hint": "timestamp",
                                                                                             "expression": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"}},
                            "operators": ["=", ">", "<", "between", "exists", "not exists", "older than",
                                          "newer than", "within last"], "sortable": True, "filterable": True,
                            "weight": 0.0,
                            "object_types": ["ACCOUNT", "APPLICATION", "CONTAINER", "GENERAL", "DEVICE", "GROUP",
                                             "STORAGE", "RESOURCE", "ROLE"],
                            "description": "# First Observation Date\n## The date when an asset was first discovered by Tenable\n\nThe first observation date is the date when an asset was first discovered by Tenable. This date is important because it can be used to track the asset's history and to identify any changes that have been made to it. The first observation date can also be used to determine the asset's age, which can be a factor in assessing its risk.\n\nHere are some key points to understand about the first observation date:\n- **Accuracy**: The first observation date is typically accurate to within a few days. However, there may be some cases where the date is not accurate, such as when an asset is discovered by Tenable but is not immediately added to the database.\n- **Relevance**: The first observation date is relevant to asset management because it can be used to track the asset's history and to identify any changes that have been made to it. The first observation date can also be used to determine the asset's age, which can be a factor in assessing its risk.\n- **Usefulness**: The first observation date can be used in a variety of ways, such as:\n    * Tracking the asset's history\n    * Identifying any changes that have been made to the asset\n    * Determining the asset's age\n    * Assessing the asset's risk\n"},
                           {"key": "acr", "readable_name": "ACR",
                            "control": {"type": "NUMBER", "multiple_allowed": False,
                                        "regex": {"hint": "a number between 1 and 10",
                                                  "expression": "^([1-9]|10)$"}},
                            "operators": ["=", ">=", ">", "<=", "<", "exists", "not exists"], "sortable": True,
                            "filterable": True, "weight": 1.0,
                            "object_types": ["ACCOUNT", "APPLICATION", "CONTAINER", "GENERAL", "DEVICE", "GROUP",
                                             "STORAGE",
                                             "RESOURCE", "ROLE"],
                            "description": "# ACR\n## Asset Criticality Rating\n\nThe Asset Criticality Rating (ACR) is a score that indicates the importance of an asset to an organization. The ACR is calculated based on a variety of factors, including the asset's sensitivity, its impact on business operations, and its potential for exploitation.\n\nThe ACR is used to prioritize assets for security and risk management. Assets with a high ACR should be given the highest priority for security controls and monitoring.\n\nHere are some key points to understand about the ACR:\n- The ACR is a numeric score that ranges from 0 to 100.\n- A higher ACR indicates a higher level of criticality.\n- The ACR is calculated using a variety of factors, including the asset's sensitivity, its impact on business operations, and its potential for exploitation.\n- The ACR is used to prioritize assets for security and risk management.\n- Assets with a high ACR should be given the highest priority for security controls and monitoring.\n"},
                           {"key": "is_licensed", "readable_name": "Is Licensed",
                            "control": {"type": "BOOLEAN", "multiple_allowed": False},
                            "operators": ["=", "!=", "exists", "not exists"], "sortable": True, "filterable": True,
                            "weight": 0.0,
                            "object_types": ["ACCOUNT", "APPLICATION", "CONTAINER", "GENERAL", "DEVICE", "GROUP",
                                             "STORAGE", "RESOURCE", "ROLE"],
                            "description": "# Is Licensed (legacy)\n## A property indicating if the asset is licensed\n\nThis property indicates whether the asset is licensed. This is a legacy property that is no longer used.\n"}]}


@pytest.fixture
def assets_response() -> dict:
    return {
        "values": [
            {
                "id": "00106d8f-e993-5ac7-bd2c-3225c8f5def7",
                "asset_class": "IAC",
                "name": "accurics_1669914793_elb",
                "aes": 0,
                "acr": 0,
                "extra_properties": {}
            }], "total_count": 1868, "offset": 0, "limit": 100, "sort_by": "aes", "sort_direction": "DESC"}


@responses.activate
def test_properties_list(tenable_exposure_management_api, asset_properties_response):
    # Arrange
    asset_classes = [AssetClass.ACCOUNT, AssetClass.DEVICE]
    asset_classes_str = ",".join([asset_class.value for asset_class in asset_classes])
    responses.get('https://cloud.tenable.com/api/v1/em/inventory/assets/properties',
                  json=asset_properties_response,
                  match=[responses.matchers.query_param_matcher({"asset_classes": asset_classes_str})])
    # Act
    asset_properties_result: list[Field] = tenable_exposure_management_api.inventory.assets.list_properties(
        asset_classes=asset_classes)
    # Assert
    assert asset_properties_result == Properties(**asset_properties_response).properties


@responses.activate
def test_list(tenable_exposure_management_api, assets_response):
    query_text = "accurics"
    query_mode = QueryMode.SIMPLE
    filters = [PropertyFilter(property="property", operator=Operator.EQUAL, value=["value"])]

    extra_properties = ["apa_asset_total_paths_count"]
    offset = 0
    limit = 100
    sort_by = "aes"
    sort_direction = SortDirection.DESC
    timezone = "America/Chicago"

    # Construct the dictionary using variables
    payload = {
        "search": {
            "query": {
                "text": query_text,
                "mode": query_mode.value
            },
            "filters": [filter.model_dump(mode='json') for filter in filters]
        },
        "extra_properties": extra_properties,
        "offset": offset,
        "limit": limit,
        "sort_by": sort_by,
        "sort_direction": sort_direction.value,
        "timezone": timezone
    }
    responses.add(responses.POST,
                  'https://cloud.tenable.com/api/v1/em/inventory/assets',
                  json=assets_response,
                  match=[responses.matchers.body_matcher(params=json.dumps(payload))])
    # Act
    assets: Assets = tenable_exposure_management_api.inventory.assets.list(query_text=query_text, query_mode=query_mode,
                                                                           filters=filters,
                                                                           extra_properties=extra_properties,
                                                                           offset=offset, limit=limit, sort_by=sort_by,
                                                                           sort_direction=sort_direction,
                                                                           timezone=timezone)
    # Assert
    assert assets == Assets(**assets_response)
