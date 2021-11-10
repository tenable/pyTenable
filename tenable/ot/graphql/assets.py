'''
Assets GraphQL API.
For each class, please refer to the Tenable.ot documentation website for a
detailed explanation of the fields.
'''
from dataclasses import dataclass
from typing import List
from marshmallow import fields
from marshmallow.decorators import post_load
from marshmallow.schema import Schema

ASSETS_QUERY_OBJECT_NAME = 'assets'
ASSETS_QUERY = '''
query assets($filter: AssetExpressionsParams, $search: String,
$sort: [AssetSortParams!]!, $limit: Int, $startAt: String) {
  assets(filter: $filter, search: $search, sort: $sort, first: $limit,
  after: $startAt){
    pageInfo{
      endCursor
    }
    nodes{
      id
      slot
      name
      type
      risk{
        unresolvedEvents
        totalRisk
      }
      criticality
      ips{
        nodes
      }
      macs{
        nodes
      }
      category
      vendor
      family
      model
      firmwareVersion
      os
      runStatus
      purdueLevel
      firstSeen
      lastSeen
      location
      backplane{
        id
        name
        size
      }
      description
      segments{
        nodes{
          id
          name
          type
          key
          systemName
          vlan
          description
          assetType
          subnet
        }
      }
    }
  }
}
'''


class RiskSchema(Schema):
    '''
    Schema for retrieving asset's risk information.
    '''
    unresolved_events = fields.Int(required=True, data_key="unresolvedEvents")
    total_risk = fields.Float(required=True, data_key="totalRisk")

    @post_load
    def to_object(self, data, **kwargs):
        '''This method turns the schema into its corresponding object.'''
        return Risk(**data)


class IpsSchema(Schema):
    '''
    Schema for retrieving a list of IP addresses.
    '''
    nodes = fields.List(fields.Str())

    @post_load
    def get_nodes(self, data, **kwargs):
        '''This method returns the list inside 'nodes' instead of an
        element.'''
        return data['nodes']


class MacsSchema(Schema):
    '''
    Schema for retrieving a list of MAC addresses.
    '''
    nodes = fields.List(fields.Str())

    @post_load
    def get_nodes(self, data, **kwargs):
        '''This method returns the list inside 'nodes' instead of an
        element.'''
        return data['nodes']


class BackplaneSchema(Schema):
    '''
    Schema for retrieving backplane information.
    '''
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    size = fields.Int(required=True)

    @post_load
    def to_object(self, data, **kwargs):
        '''This method turns the schema into its corresponding object.'''
        return Backplane(**data)


class SegmentSchema(Schema):
    '''
    Schema for retrieving segment information.
    '''
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    type = fields.Str(required=True)
    key = fields.Str(required=True)
    system_name = fields.Str(allow_none=True, data_key="systemName")
    vlan = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
    asset_type = fields.Str(allow_none=True, data_key="assetType")
    subnet = fields.Str(allow_none=True)

    @post_load
    def to_object(self, data, **kwargs):
        '''This method turns the schema into its corresponding object.'''
        return Segment(**data)


class SegmentsSchema(Schema):
    '''
    Schema for retrieving a list of segments.
    '''
    nodes = fields.List(fields.Nested(SegmentSchema))

    @post_load
    def get_nodes(self, data, **kwargs):
        '''This method returns the list inside 'nodes' instead of an
        element.'''
        return data['nodes']


class AssetSchema(Schema):
    '''
    Schema for retrieving asset information.
    '''
    id = fields.Str(required=True)
    slot = fields.Int(allow_none=True)
    name = fields.Str(required=True)
    type = fields.Str(required=True)
    risk = fields.Nested(RiskSchema, required=True)
    criticality = fields.Str(required=True)
    ips = fields.Nested(IpsSchema, allow_none=True)
    macs = fields.Nested(MacsSchema, allow_none=True)
    category = fields.Str(required=True)
    vendor = fields.Str(allow_none=True)
    family = fields.Str(allow_none=True)
    model = fields.Str(allow_none=True)
    firmware_version = fields.Str(allow_none=True, data_key="firmwareVersion")
    os = fields.Str(allow_none=True)
    run_status = fields.Str(allow_none=True, data_key="runStatus")
    purdue_level = fields.Str(required=True, data_key="purdueLevel")
    first_seen = fields.Str(allow_none=True, data_key="firstSeen")
    last_seen = fields.Str(allow_none=True, data_key="lastSeen")
    location = fields.Str(allow_none=True)
    backplane = fields.Nested(BackplaneSchema, allow_none=True)
    description = fields.Str(allow_none=True)
    segments = fields.Nested(SegmentsSchema, allow_none=True)

    @post_load
    def to_object(self, data, **kwargs):
        '''This method turns the schema into its corresponding object.'''
        return Asset(**data)


class AssetsSchema(Schema):
    '''
    Schema for retrieving a list of assets.
    '''
    nodes = fields.List(fields.Nested(AssetSchema))

    @post_load
    def get_nodes(self, data, **kwargs):
        '''This method returns the list inside 'nodes' instead of an
        element.'''
        return data['nodes']


@dataclass
class Risk:
    '''
    This class holds the risk information.
    '''
    unresolved_events: int
    total_risk: float


@dataclass
class Ips:
    '''
    This class holds a list of IP addresses.
    '''
    ips: List[str]


@dataclass
class Macs:
    '''
    This class holds a list of MAC addresses.
    '''
    macs: List[str]


@dataclass
class Backplane:
    '''
    This class holds a backplane's information.
    '''
    id: str
    name: str
    size: str


@dataclass
class Segment:
    '''
    This class holds a segment's information.
    '''
    id: str
    name: str
    type: str
    key: str
    system_name: str = None
    vlan: str = None
    description: str = None
    asset_type: str = None
    subnet: str = None


@dataclass
class Asset:
    '''
    This class holds Tenable.ot asset information.
    '''
    id: str
    name: str
    type: str
    risk: Risk
    criticality: str
    category: str
    purdue_level: str
    slot: int = None
    ips: Ips = None
    macs: Macs = None
    vendor: str = None
    family: str = None
    model: str = None
    firmware_version: str = None
    os: str = None
    run_status: str = None
    first_seen: str = None
    last_seen: str = None
    location: str = None
    backplane: Backplane = None
    description: str = None
    segments: List[Segment] = None
