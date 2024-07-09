

ASSETS = '''
 query getAssets(
  $filter: AssetExpressionsParams
  $search: String
  $limit: Int
  $sort: [AssetSortParams!]!
  $startAt: String
) {
  assets(
    filter: $filter
    sort: $sort
    search: $search
    first: $limit
    after: $startAt
  ) {
    pageInfo {
      endCursor
    }
    nodes {
      ...inventoryAsset
    }
    count: totalCount
  }
}
fragment inventoryAsset on Asset {
  details
}
'''


FINDING_ASSETS = '''
query getAssets(
  $filter: AssetExpressionsParams
  $search: String
  $limit: Int
  $sort: [AssetSortParams!]!
  $startAt: String
) {
  assets(
    filter: $filter
    sort: $sort
    search: $search
    first: $limit
    after: $startAt
  ) {
    pageInfo {
      endCursor
    }
    count: totalCount
    nodes {
      id
    }
  }
}
'''


PLUGINS = '''
query getAssets(
  $filter: PluginExpressionsParams
  $search: String
  $limit: Int
  $sort: [PluginSortParams!]!
  $startAt: String
) {
  plugins(
    filter: $filter
    sort: $sort
    search: $search
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
      details {
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
        cves
        cpes
        cvssVector
        cvssV3Vector
        cvssTemporalVector
        cvssV3TemporalVector
        cvssBaseScore
        cvssV3BaseScore
        cvssTemporalScore
        cvssV3TemporalScore
        stigSeverity
        scriptVersion
        exploitAvailable
        exploitabilityEase
        exploitedByMalware
        exploitFrameworkCore
        exploitFrameworkCanvas
        exploitFrameworkD2Elliot
        exploitFrameworkExploithub
        exploitFrameworkMetasploit
        canvasPackage
        exploithubSku
        metasploitName
        d2ElliotName
        threatRecency
        threatIntensity
        exploitCodeMaturity
        ageOfVuln
        productCoverage
      }
    }
  }
}
'''

CONNECTIONS_BETWEEN_ASSETS = '''
  query getLinks(
    $filter: LinkExpressionsParams, 
    $search: String, 
    $sort: [LinkSortParams!]!, 
    $limit: Int, 
    $after: String
    ) {
    links(
      filter: $filter
      search: $search
      sort: $sort
      after: $after
      first: $limit
    ) {
      pageInfo{
        endCursor
      }
      nodes {
        conversationLinkId: id
        asset1
        asset2
        protocols {
          nodes {
            name
            isICSProtocol:ics
            __typename
          }
          __typename
        }
        numConversations: convCount
        firstConversationTime: firstConv
        lastConversationTime: lastConv
      }
    }
}
'''
