"""
OT GraphQL API Queries.
For each class, please refer to the Tenable.ot documentation website for a
detailed explanation of the fields.
"""

"""
GraphQL query for Tenable.OT assets.
"""
ASSETS_QUERY = """
query assets(
  $filter: AssetExpressionsParams
  $search: String
  $sort: [AssetSortParams!]!
  $limit: Int
  $startAt: String
) {
  assets(
    filter: $filter
    search: $search
    sort: $sort
    first: $limit
    after: $startAt
  ) {
    pageInfo {
      endCursor
    }
    nodes {
      category
      criticality
      customField1
      customField2
      customField3
      customField4
      customField5
      customField6
      customField7
      customField8
      customField9
      customField10
      description
      details
      family
      firmwareVersion
      firstSeen
      hidden
      id
      ips {
        nodes
      }
      lastSeen
      lastUpdate
      location
      macs {
        nodes
      }
      model
      name
      os
      osDetails {
        name
        architecture
        hotFixes {
          nodes {
            name
            installDate
            description
          }
        }
        version
      }
      purdueLevel
      runStatus
      runStatusTime
      serial
      slot
      superType
      type
      vendor
      risk {
        unresolvedEvents
        totalRisk
      }
      ips {
        nodes
      }
      macs {
        nodes
      }
      backplane {
        id
        name
        size
      }
      segments {
        nodes {
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
      revisions {
        nodes {
          id
          firstSeen
          lastSeen
          ordinal
          isBase
        }
      }
    }
  }
}
"""
