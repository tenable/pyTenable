"""
Findings
========

Methods described in this section relate to the findings API.
These methods can be accessed at ``TenableOT.findings``.

Findings represent detected vulnerabilities (plugins) on assets in your OT environment.

.. rst-class:: hide-signature
.. autoclass:: FindingsAPI
    :members:
"""
from typing import List, Optional

from tenable.ot.api import OTAPIBase
from tenable.ot.graphql.iterators import OTGraphIterator
from tenable.ot.graphql.query import FINDINGS_QUERY
from tenable.ot.graphql.schema.findings import FindingsSchema


class FindingsAPI(OTAPIBase):
    """
    API interface for managing and retrieving security findings.

    A finding represents a detected vulnerability (plugin) on a specific asset.
    """
    _path = "findings"
    query = FINDINGS_QUERY
    schema_class = FindingsSchema

    def list(
        self,
        query_filter: Optional[dict] = None,
        search: Optional[str] = None,
        sort: Optional[List[dict]] = None,
        start_at: Optional[str] = None,
        limit: Optional[int] = 200,
        **kwargs,
    ) -> OTGraphIterator:
        """
        Retrieves a list of findings via the GraphQL API.

        A finding represents a vulnerability detected on an asset. Each finding
        includes information about the affected asset, the detected plugin/vulnerability,
        detection timestamps, and current status.

        Args:
            query_filter(dict, optional):
                A filter document as defined by Tenable OT Security documentation.
                Common filter fields include:
                - assetId: Filter by specific asset UUID
                - pluginId: Filter by specific plugin ID
                - findingStatus: Filter by status (Active, Resolved, Resurfaced)
                - pluginSeverity: Filter by severity (Critical, High, Medium, Low, Info)

                Example filter for a specific asset:
                    {"field": "assetId", "op": "Equal", "values": "uuid-here"}

                Example filter for active critical findings:
                    {
                        "op": "And",
                        "expressions": [
                            {"field": "findingStatus", "op": "Equal", "values": "Active"},
                            {"field": "pluginSeverity", "op": "Equal", "values": "Critical"}
                        ]
                    }

            search(str, optional):
                A search string to further limit the response. Searches across
                finding fields like plugin name, asset name, etc.

            sort(List[dict], optional):
                A list of sort parameters. Each dict should contain 'field' and
                'direction' keys. Available directions: AscNullFirst, AscNullLast,
                DescNullFirst, DescNullLast.

                Example:
                    [{"field": "findingLastHit", "direction": "DescNullLast"}]

                Common sort fields:
                - findingLastHit: Sort by when finding was last detected
                - findingFirstHit: Sort by when finding was first detected
                - pluginSeverity: Sort by plugin severity
                - assetName: Sort by asset name

            start_at(str, optional):
                The cursor to start the scan from (for pagination).

            limit(int, optional):
                Max number of findings to retrieve per page (default: 200).

        Returns:
            :obj:`OTGraphIterator`:
                An iterator object that handles pagination of findings data.

        Examples:
            List all findings:

            >>> for finding in tot.findings.list():
            ...     print(f"{finding.asset.name}: {finding.plugin.name} [{finding.status}]")

            Get findings for a specific asset:

            >>> asset_id = "5cb025fd-524b-47f1-81f7-bd472b450c7d"
            >>> findings = tot.findings.list(
            ...     query_filter={
            ...         "field": "assetId",
            ...         "op": "Equal",
            ...         "values": asset_id
            ...     }
            ... )
            >>> for finding in findings:
            ...     print(finding.plugin.name)

            Get active critical findings:

            >>> findings = tot.findings.list(
            ...     query_filter={
            ...         "op": "And",
            ...         "expressions": [
            ...             {"field": "findingStatus", "op": "Equal", "values": "Active"},
            ...             {"field": "pluginSeverity", "op": "Equal", "values": "Critical"}
            ...         ]
            ...     },
            ...     sort=[{"field": "findingLastHit", "direction": "DescNullLast"}]
            ... )

            Get findings detected in the last 7 days:

            >>> from datetime import datetime, timedelta
            >>> seven_days_ago = (datetime.now() - timedelta(days=7)).isoformat()
            >>> findings = tot.findings.list(
            ...     query_filter={
            ...         "field": "findingLastHit",
            ...         "op": "GreaterThan",
            ...         "values": seven_days_ago
            ...     }
            ... )
        """
        # Default sort: most recently detected findings first, then by ID
        if not sort:
            sort = [
                {"field": "findingLastHit", "direction": "DescNullLast"},
                {"field": "findingId", "direction": "AscNullLast"}
            ]

        return super().list(
            query=FINDINGS_QUERY,
            query_filter=query_filter,
            search=search,
            sort=sort,
            start_at=start_at,
            limit=limit,
            **kwargs,
        )

    def finding(
        self,
        finding_id: str,
        **kwargs,
    ) -> OTGraphIterator:
        """
        Retrieve a specific finding by ID.

        Args:
            finding_id (str):
                The finding ID (SHA256 hash string).

        Returns:
            :obj:`OTGraphIterator`:
                An iterator object handling data pagination. Note: even though
                this retrieves a single finding, it returns an iterator for
                consistency with the API design.

        Example:
            >>> finding_id = "d9dc32ba06243f814f819d363b521d55e351d9370b17c750c6322a67bc9d0086"
            >>> findings = tot.findings.finding(finding_id)
            >>> for finding in findings:
            ...     print(f"Plugin: {finding.plugin.name}")
            ...     print(f"Asset: {finding.asset.name}")
            ...     print(f"Status: {finding.status}")
        """
        return super().list(
            query_filter={
                "field": "findingId",
                "op": "Equal",
                "values": finding_id,
            },
            query=FINDINGS_QUERY,
            **kwargs,
        )

    def by_asset(
        self,
        asset_id: str,
        status: Optional[str] = None,
        severity: Optional[str] = None,
        sort: Optional[List[dict]] = None,
        limit: Optional[int] = 200,
        **kwargs,
    ) -> OTGraphIterator:
        """
        Retrieve all findings for a specific asset.

        This is a convenience method that simplifies getting findings for an asset
        with optional filtering by status and severity.

        Args:
            asset_id (str):
                The asset UUID to retrieve findings for.

            status (str, optional):
                Filter by finding status. Valid values: Active, Resolved, Resurfaced.

            severity (str, optional):
                Filter by plugin severity. Valid values: Critical, High, Medium, Low, Info.

            sort (List[dict], optional):
                Sort parameters. Defaults to most recently detected first.

            limit (int, optional):
                Max number of findings per page (default: 200).

        Returns:
            :obj:`OTGraphIterator`:
                An iterator object for the findings.

        Examples:
            Get all findings for an asset:

            >>> asset_id = "5cb025fd-524b-47f1-81f7-bd472b450c7d"
            >>> findings = tot.findings.by_asset(asset_id)
            >>> print(f"Found {len(list(findings))} findings")

            Get only active critical findings for an asset:

            >>> findings = tot.findings.by_asset(
            ...     asset_id="5cb025fd-524b-47f1-81f7-bd472b450c7d",
            ...     status="Active",
            ...     severity="Critical"
            ... )
        """
        # Build filter expressions
        expressions = [
            {"field": "assetId", "op": "Equal", "values": asset_id}
        ]

        if status:
            expressions.append(
                {"field": "findingStatus", "op": "Equal", "values": status}
            )

        if severity:
            expressions.append(
                {"field": "pluginSeverity", "op": "Equal", "values": severity}
            )

        # If only one expression, use it directly, otherwise use And operator
        query_filter = expressions[0] if len(expressions) == 1 else {
            "op": "And",
            "expressions": expressions
        }

        return self.list(
            query_filter=query_filter,
            sort=sort,
            limit=limit,
            **kwargs,
        )

    def by_plugin(
        self,
        plugin_id: int,
        status: Optional[str] = None,
        sort: Optional[List[dict]] = None,
        limit: Optional[int] = 200,
        **kwargs,
    ) -> OTGraphIterator:
        """
        Retrieve all findings for a specific plugin/vulnerability.

        This shows all assets affected by a particular vulnerability.

        Args:
            plugin_id (int):
                The plugin ID to retrieve findings for.

            status (str, optional):
                Filter by finding status. Valid values: Active, Resolved, Resurfaced.

            sort (List[dict], optional):
                Sort parameters. Defaults to most recently detected first.

            limit (int, optional):
                Max number of findings per page (default: 200).

        Returns:
            :obj:`OTGraphIterator`:
                An iterator object for the findings.

        Examples:
            Get all assets affected by a specific vulnerability:

            >>> plugin_id = 502387
            >>> findings = tot.findings.by_plugin(plugin_id)
            >>> affected_assets = {f.asset.name for f in findings}
            >>> print(f"Vulnerability affects {len(affected_assets)} assets")

            Get only active findings for a plugin:

            >>> findings = tot.findings.by_plugin(
            ...     plugin_id=502387,
            ...     status="Active"
            ... )
        """
        # Build filter expressions
        expressions = [
            {"field": "pluginId", "op": "Equal", "values": plugin_id}
        ]

        if status:
            expressions.append(
                {"field": "findingStatus", "op": "Equal", "values": status}
            )

        # If only one expression, use it directly, otherwise use And operator
        query_filter = expressions[0] if len(expressions) == 1 else {
            "op": "And",
            "expressions": expressions
        }

        return self.list(
            query_filter=query_filter,
            sort=sort,
            limit=limit,
            **kwargs,
        )
