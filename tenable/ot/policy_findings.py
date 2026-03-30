"""
Policy Findings
===============

Methods described in this section relate to the policy findings API.
These methods can be accessed at ``TenableOT.policy_findings``.

Policy findings represent policy violations detected in your OT environment.
Each finding groups related policy violation events together.

.. rst-class:: hide-signature
.. autoclass:: PolicyFindingsAPI
    :members:
"""
from typing import List, Optional

from tenable.ot.api import OTAPIBase
from tenable.ot.graphql.iterators import OTGraphIterator
from tenable.ot.graphql.query import POLICY_FINDINGS_QUERY
from tenable.ot.graphql.schema.policy_findings import PolicyFindingsSchema


class PolicyFindingsAPI(OTAPIBase):
    """
    API interface for managing and retrieving policy violation findings.

    A policy finding represents one or more policy violation events grouped together,
    showing what policies were violated and which assets were involved.
    """
    _path = "policyFindings"
    query = POLICY_FINDINGS_QUERY
    schema_class = PolicyFindingsSchema

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
        Retrieves a list of policy findings via the GraphQL API.

        A policy finding represents grouped policy violation events showing what
        policies were violated, by which assets, and when. Each finding can contain
        multiple related policy hits.

        Args:
            query_filter(dict, optional):
                A filter document as defined by Tenable OT Security documentation.
                Common filter fields include:
                - id: Filter by specific policy finding ID
                - policyId: Filter by specific policy ID
                - eventType: Filter by event type
                - category: Filter by category
                - severity: Filter by severity (Critical, High, Medium, Low, Info)
                - status: Filter by status (Active, Resolved, Resurfaced)
                - srcAssets: Filter by source asset IDs
                - dstAssets: Filter by destination asset IDs
                - firstHitTime: Filter by first hit timestamp
                - lastHitTime: Filter by last hit timestamp

                Example filter for a specific policy:
                    {"field": "policyId", "op": "Equal", "values": "policy-uuid"}

                Example filter for active high severity findings:
                    {
                        "op": "And",
                        "expressions": [
                            {"field": "status", "op": "Equal", "values": "Active"},
                            {"field": "severity", "op": "Equal", "values": "High"}
                        ]
                    }

            search(str, optional):
                A search string to further limit the response.

            sort(List[dict], optional):
                A list of sort parameters. Each dict should contain 'field' and
                'direction' keys.

                Example:
                    [{"field": "lastHitTime", "direction": "DescNullLast"}]

                Common sort fields:
                - lastHitTime: Sort by most recent activity
                - firstHitTime: Sort by when first detected
                - severity: Sort by severity level
                - policyTitle: Sort by policy title

            start_at(str, optional):
                The cursor to start the scan from (for pagination).

            limit(int, optional):
                Max number of findings to retrieve per page (default: 200).

        Returns:
            :obj:`OTGraphIterator`:
                An iterator object that handles pagination of policy findings data.

        Examples:
            List all policy findings:

            >>> for finding in tot.policy_findings.list():
            ...     print(f"{finding.policy_title}: {finding.severity} [{finding.status}]")
            ...     print(f"  Source: {finding.src_names}")
            ...     print(f"  Destination: {finding.dst_names}")
            ...     print(f"  Active hits: {finding.active_policy_hits}")

            Get active critical policy findings:

            >>> findings = tot.policy_findings.list(
            ...     query_filter={
            ...         "op": "And",
            ...         "expressions": [
            ...             {"field": "status", "op": "Equal", "values": "Active"},
            ...             {"field": "severity", "op": "Equal", "values": "Critical"}
            ...         ]
            ...     },
            ...     sort=[{"field": "lastHitTime", "direction": "DescNullLast"}]
            ... )

            Get findings for a specific policy:

            >>> policy_id = "1ab9c93c-3114-4f60-9f3d-d88ba33d332a"
            >>> findings = tot.policy_findings.list(
            ...     query_filter={"field": "policyId", "op": "Equal", "values": policy_id}
            ... )

            Get recent policy findings (last 7 days):

            >>> from datetime import datetime, timedelta
            >>> seven_days_ago = (datetime.now() - timedelta(days=7)).isoformat()
            >>> findings = tot.policy_findings.list(
            ...     query_filter={
            ...         "field": "lastHitTime",
            ...         "op": "GreaterThan",
            ...         "values": seven_days_ago
            ...     }
            ... )
        """
        # Default sort: most recently active findings first
        if not sort:
            sort = [
                {"field": "lastHitTime", "direction": "DescNullLast"},
                {"field": "id", "direction": "AscNullLast"}
            ]

        return super().list(
            query=POLICY_FINDINGS_QUERY,
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
        Retrieve a specific policy finding by ID.

        Args:
            finding_id (str):
                The policy finding UUID.

        Returns:
            :obj:`OTGraphIterator`:
                An iterator object handling data pagination.

        Example:
            >>> finding_id = "f5fdbd87-993d-4d81-84b6-ba94fa4f5fe8"
            >>> findings = tot.policy_findings.finding(finding_id)
            >>> for finding in findings:
            ...     print(f"Policy: {finding.policy_title}")
            ...     print(f"Status: {finding.status}")
            ...     print(f"Active hits: {finding.active_policy_hits}")
        """
        return super().list(
            query_filter={
                "field": "id",
                "op": "Equal",
                "values": finding_id,
            },
            query=POLICY_FINDINGS_QUERY,
            **kwargs,
        )

    def by_policy(
        self,
        policy_id: str,
        status: Optional[str] = None,
        severity: Optional[str] = None,
        sort: Optional[List[dict]] = None,
        limit: Optional[int] = 200,
        **kwargs,
    ) -> OTGraphIterator:
        """
        Retrieve all findings for a specific policy.

        This is a convenience method to get all violations of a specific policy
        with optional filtering by status and severity.

        Args:
            policy_id (str):
                The policy UUID to retrieve findings for.

            status (str, optional):
                Filter by finding status. Valid values: Active, Resolved, Resurfaced.

            severity (str, optional):
                Filter by severity. Valid values: Critical, High, Medium, Low, Info.

            sort (List[dict], optional):
                Sort parameters. Defaults to most recently active first.

            limit (int, optional):
                Max number of findings per page (default: 200).

        Returns:
            :obj:`OTGraphIterator`:
                An iterator object for the findings.

        Examples:
            Get all findings for a policy:

            >>> policy_id = "1ab9c93c-3114-4f60-9f3d-d88ba33d332a"
            >>> findings = tot.policy_findings.by_policy(policy_id)
            >>> print(f"Policy has {len(list(findings))} findings")

            Get only active critical findings for a policy:

            >>> findings = tot.policy_findings.by_policy(
            ...     policy_id="1ab9c93c-3114-4f60-9f3d-d88ba33d332a",
            ...     status="Active",
            ...     severity="Critical"
            ... )
        """
        # Build filter expressions
        expressions = [
            {"field": "policyId", "op": "Equal", "values": policy_id}
        ]

        if status:
            expressions.append(
                {"field": "status", "op": "Equal", "values": status}
            )

        if severity:
            expressions.append(
                {"field": "severity", "op": "Equal", "values": severity}
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

    def by_asset(
        self,
        asset_id: str,
        direction: str = "both",
        status: Optional[str] = None,
        severity: Optional[str] = None,
        sort: Optional[List[dict]] = None,
        limit: Optional[int] = 200,
        **kwargs,
    ) -> OTGraphIterator:
        """
        Retrieve all policy findings involving a specific asset.

        This shows all policy violations where the asset was involved as either
        a source, destination, or both.

        Args:
            asset_id (str):
                The asset UUID to retrieve findings for.

            direction (str, optional):
                Filter by asset role. Valid values:
                - "both": Asset as source or destination (default)
                - "source": Asset as source only
                - "destination": Asset as destination only

            status (str, optional):
                Filter by finding status. Valid values: Active, Resolved, Resurfaced.

            severity (str, optional):
                Filter by severity. Valid values: Critical, High, Medium, Low, Info.

            sort (List[dict], optional):
                Sort parameters. Defaults to most recently active first.

            limit (int, optional):
                Max number of findings per page (default: 200).

        Returns:
            :obj:`OTGraphIterator`:
                An iterator object for the findings.

        Examples:
            Get all policy findings involving an asset:

            >>> asset_id = "51844e94-48d1-4185-98d4-0b962ec5b966"
            >>> findings = tot.policy_findings.by_asset(asset_id)
            >>> for finding in findings:
            ...     print(f"{finding.policy_title}: {finding.severity}")

            Get findings where asset was the source:

            >>> findings = tot.policy_findings.by_asset(
            ...     asset_id="51844e94-48d1-4185-98d4-0b962ec5b966",
            ...     direction="source"
            ... )

            Get active critical findings involving asset:

            >>> findings = tot.policy_findings.by_asset(
            ...     asset_id="51844e94-48d1-4185-98d4-0b962ec5b966",
            ...     status="Active",
            ...     severity="Critical"
            ... )
        """
        # Build asset filter based on direction
        if direction == "source":
            asset_filter = {"field": "srcAssets", "op": "Equal", "values": asset_id}
        elif direction == "destination":
            asset_filter = {"field": "dstAssets", "op": "Equal", "values": asset_id}
        else:  # both
            asset_filter = {
                "op": "Or",
                "expressions": [
                    {"field": "srcAssets", "op": "Equal", "values": asset_id},
                    {"field": "dstAssets", "op": "Equal", "values": asset_id}
                ]
            }

        # Build additional filters
        expressions = [asset_filter]

        if status:
            expressions.append(
                {"field": "status", "op": "Equal", "values": status}
            )

        if severity:
            expressions.append(
                {"field": "severity", "op": "Equal", "values": severity}
            )

        # If only asset filter, use it directly, otherwise use And operator
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
