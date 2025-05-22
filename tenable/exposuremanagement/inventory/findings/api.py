from typing import Optional

from tenable.base.endpoint import APIEndpoint
from tenable.exposuremanagement.inventory.findings.schema import Findings
from tenable.exposuremanagement.inventory.schema import Field, Properties, QueryMode, PropertyFilter, SortDirection


class FindingsAPI(APIEndpoint):
    def list_properties(self) -> list[Field]:
        """
             Retrieve finding properties

            Returns:
                The finding properties.

             Examples:
                 >>> tenable_inventory_finding_properties = tenable_inventory.finding.list_properties()
                 >>> for finding_property in tenable_inventory_finding_properties:
                 ...     pprint(finding_property)

        """
        finding_properties_response: dict[str, list[dict]] = self._get(
            path='inventory/api/v1/findings/properties'
        )
        return Properties(**finding_properties_response).properties

    def list(
            self,
            query_text: Optional[str] = None,
            query_mode: Optional[QueryMode] = None,
            filters: Optional[list[PropertyFilter]] = None,
            extra_properties: Optional[list[str]] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            sort_by: Optional[str] = None,
            sort_direction: Optional[SortDirection] = None,
            timezone: Optional[str] = None,
    ) -> Findings:
        """
         Retrieve findings

         Args:
            query_text (str, optional):
                The text to search for.
            query_mode (QueryMode, optional):
                The search mode. Defaults to QueryMode.SIMPLE.
            filters (list, optional):
                A list of filters to apply. Defaults to None.
            extra_properties (list, optional):
                Additional properties to include in the response. Defaults to None.
            offset (int, optional):
                Number of records to skip. Defaults to 0.
            limit (int, optional):
                Maximum number of records per page. Defaults to 1000.
            sort_by (str, optional):
                Field to sort by.
            sort_direction (SortDirection, optional):
                Sorting direction, either SortDirection.ASC or SortDirection.DESC.
            timezone (str, optional):
                Timezone setting for the query. Defaults to "UTC".

        Returns:
            The request assets.

         Examples:
             >>> tenable_inventory_findings = tenable_inventory.finding.list()
             >>> for finding in tenable_inventory_findings:
             ...     pprint(finding)

        """
        payload = {}

        if query_text is not None and query_mode is not None and filters is not None:
            payload['search'] = {
                'query': {'text': query_text, 'mode': query_mode.value},
                'filters': [filter_.model_dump(mode='json') for filter_ in filters]
                if filters is not None
                else [],
            }

        if extra_properties is not None:
            payload['extra_properties'] = extra_properties
        if offset is not None:
            payload['offset'] = offset
        if limit is not None:
            payload['limit'] = limit
        if sort_by is not None:
            payload['sort_by'] = sort_by
        if sort_direction is not None:
            payload['sort_direction'] = sort_direction.value
        if timezone is not None:
            payload['timezone'] = timezone

        findings_response: dict = self._post('inventory/api/v1/findings', json=payload)
        return Findings(**findings_response)