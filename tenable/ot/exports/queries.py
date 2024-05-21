

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
