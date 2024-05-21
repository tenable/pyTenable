"""
OT GraphQL API Queries.
For each class, please refer to the Tenable OT Security documentation website for a
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
      plugins {
        nodes {
          id
          name
          source
          family
          severity
          vprScore
          comment
          owner
          totalAffectedAssets
        }
      }
    }
  }
}
"""

"""
GraphQL query for Tenable.OT plugins.
"""
PLUGINS_QUERY = """
query plugins(
  $filter: PluginExpressionsParams
  $search: String
  $sort: [PluginSortParams!]!
  $limit: Int
  $startAt: String
) {
  plugins(
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
      id
      name
      source
      family
      severity
      vprScore
      comment
      owner
      totalAffectedAssets
      affectedAssets {
        nodes {
          id
          name
        }
      }
    }
  }
}
"""

"""
GraphQL query for Tenable.OT plugins with additional details from NNM.
"""
PLUGINS_DETAILS_QUERY = """
query plugins(
  $filter: PluginExpressionsParams
  $search: String
  $sort: [PluginSortParams!]!
  $limit: Int
  $startAt: String
) {
  plugins(
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
      id
      name
      source
      family
      severity
      vprScore
      comment
      owner
      totalAffectedAssets
      details {
        id
        name
        source
        family
        description
        solution
        seeAlso
        pluginType
        pluginPubDate
        pluginModDate
        vulnPubDate
        vulnModDate
        refs {
          name
          value
          url
        }
        cpe
        cvssVector
        cvssV3Vector
        cvssBaseScore
        cvssV3BaseScore
        cvssV3TemporalScore
        cvssTemporalScore
        cvssV3TemporalVector
        cvssImpactScore
      }
      affectedAssets {
        nodes {
          id
          name
        }
      }
    }
  }
}
"""

"""
GraphQL query for Tenable.OT events
"""
EVENTS_QUERY = """
query events(
  $filter: EventsExpressionsParams,
  $search: String,
  $sort: [EventsSortParams!]!,
  $limit: Int,
  $startAt: String
){
  events(
    filter: $filter,
    search: $search,
    sort: $sort,
    first: $limit,
    after: $startAt
  ){
    pageInfo{
      endCursor
    }
    nodes{
    id
    eventType {
      type
      group
      description
      schema
      category
      family
      canCapture
      actions
      exclusion
    }
    srcIP
    dstIP
    protocolRaw
    policy {
      id
      index
      title
      level
      disabled
      archived
      schema
      continuous
      snapshot
      system
      key
      eventTypeDetails {
        type
        group
        description
        schema
        category
        family
        canCapture
        actions
        exclusion
      }
      disableAfterHit
         actions{
          nodes{
            aid
            type
          }
        }
      paused
      srcAssetGroup{
        group{
          id
        }
        negate
      }
      dstAssetGroup{
        group{
          id
        }
        negate
      }
      schedule{
        group{
          id
        }
        negate
      }
      protocolGroup{
        group{
          id
        }
        negate
      }
      portGroup{
        group{
          id
          name
        }
        negate
      }
      tagGroup{
        group{
          id
          name
        }
        negate
      }
      valueGroup{
        group{
          id
        }
        negate
      }
      ruleGroup{
        group{
          id
          name
        }
        negate
      }
     exclusions{
      nodes{
        id
      }
    }
      aggregatedEventsCount{
        last24h
        last7d
        last30d
      }
    }
    time
    srcMac
    dstMac
    completion
    protocolNiceName
    resolved
    resolvedTs
    hitId
    severity
    category
    comment
    logId
    resolvedUser
    type
    srcAssets{
      nodes{
        name
        id
      }
    }
    srcInterface{
      id
      lastSeen
      firstSeen
      mac
      ips {
        nodes{
          ip
        }
      }
      dnsNames{
            nodes
      }
      family
      directAsset {
        id
      }
    }
    srcNames{
      nodes
    }
    dstAssets{
      nodes{
        name
        id
      }
    }
    dstInterface{
      id
      lastSeen
      firstSeen
      mac
      ips {
        nodes{
          ip
        }
      }
      dnsNames{
            nodes
      }
      family
      directAsset {
        id
      }
    }
    dstNames{
      nodes
    }
    hasDetails
    payloadSize
    protocol
    port
    continuous
    }
  }
}
"""
