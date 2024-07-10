ASSETS = '''
 query getAssets($filter: AssetExpressionsParams, $search: String, $sort: [AssetSortParams!]!, $after: String, $limit: Int) {
  assets(
    filter: $filter
    sort: $sort
    search: $search
    after: $after
    first: $limit
  ) {
    pageInfo {
      endCursor
    }
    nodes {
      ...inventoryAsset
    }
  }
}

fragment inventoryAsset on Asset {
  id
  type
  superType
  name
  lastScanTime: lastHit
  baseRevision {
    id
    firstSeen
    lastSeen
    isBase
  }
  indirectIps: ips {
    nodes
  }
  directIps {
    nodes
  }
  indirectMacs: macs {
    nodes
  }
  directMacs {
    nodes
  }
  indirectnetworkInterfaces: networkInterfaces {
    nodes {
      id
      mac
      ips {
        nodes {
          ip
          dnsNames {
            nodes 
          }
          openPorts {
            ports {
              nodes {
                port
                source
                name
                description
              }
            }
            scannedOnce
            inOnDemandScan
          }
        }
      }
    }
  }
  directNetworkInterfaces {
    nodes {
      id
			ips {
        nodes {
          ip
          dnsNames {
            nodes 
          }
          openPorts {
            ports {
              nodes {
                port
                source
                name
                description
              }
            }
            scannedOnce
            inOnDemandScan
          }
        }
      }
      dnsNames {
         nodes 
      }
      family
      directAsset {
        id
        ips {
          nodes 
        }
        name
      }
      ipTrail {
        nodes {
          ip
          isActive
        }
      }
      
    }
  }
  category
  family
  firmwareVersion
  location
  runStatus
  model
  vendor
  description
  os
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
  slot
  backplane {
    id
    name
    size
    
		relatedAssets:assets {
      nodes {
        id
        name
        slot
      }
    }
  }
  firstSeen
  lastSeen
  lastUpdated: lastUpdate
  risk {
    totalRisk
  }
  criticality
  purdueLevel
  category
  hidden
  segments {
    nodes {
      ...segmentName
    }

  }

}

fragment segmentName on SegmentGroup {
  id
  name
  type
  archived
  system
  key
  lastModifiedBy
  lastModifiedDate
  systemName
  vlan
  description
  assetType
  subnet
  isPredefinedName
  system
  isPredefinedName
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

PAIRED_ICPS = '''
query getPairedIcps(
  $limit: Int
	$startAt: String
	){
emPairedIcps(
  first:$limit
	after:$startAt
	){
  pageInfo{
    endCursor
  }
    nodes {
      status
      site {
        name
        host
        machineId
      }
      version {
        version
      }
      license {
        status
      }
    }
  }
}
'''
