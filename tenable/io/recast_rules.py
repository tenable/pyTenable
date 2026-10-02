"""
Recast Rules
============

The following methods allow for interaction with the Tenable Vulnerability
Management Recast Rules API endpoints.

Methods available on ``tio.recast_rules``:

.. rst-class:: hide-signature
.. autoclass:: RecastRulesAPI
    :members:
"""

from typing import Any

from tenable.utils import scrub

from .base import TIOEndpoint


class RecastRulesAPI(TIOEndpoint):
    """Manage Tenable Vulnerability Management recast rules.

    Access this API through ``tio.recast_rules``. Rule values and search
    filters are passed to the API as dictionaries.
    """

    _resource_types = ['HOST', 'HOST_AUDIT', 'WEBAPP']

    def _payload(
        self,
        resource_type: str,
        rule_value: dict[str, Any],
        rule_name: str | None = None,
        description: str | None = None,
        expires_at: str | None = None,
        disabled_details: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload = {
            'resource_type': self._check(
                'resource_type', resource_type, str, choices=self._resource_types
            ),
            'rule_value': self._check('rule_value', rule_value, dict),
        }
        optional = {
            'rule_name': (rule_name, str),
            'description': (description, str),
            'expires_at': (expires_at, str),
            'disabled_details': (disabled_details, dict),
        }
        for name, (value, expected_type) in optional.items():
            if value is not None:
                payload[name] = self._check(name, value, expected_type)
        return payload

    def create(
        self,
        resource_type: str,
        rule_value: dict[str, Any],
        rule_name: str | None = None,
        description: str | None = None,
        expires_at: str | None = None,
        disabled_details: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a recast rule.

        Args:
            resource_type (str): One of ``HOST``, ``HOST_AUDIT``, or ``WEBAPP``.
            rule_value (dict): Rule criteria accepted by the Recast Rules API.
            rule_name (str, optional): Name for the rule.
            description (str, optional): Description of the rule.
            expires_at (str, optional): Expiration timestamp accepted by the API.
            disabled_details (dict, optional): API-defined disabled-rule details.

        Returns:
            dict: The created rule response from the API.

        Examples:
            Create a host rule with API-defined criteria:

            >>> tio.recast_rules.create('HOST', rule_value)
        """
        return self._api.post(
            'v1/recast/rules',
            json=self._payload(
                resource_type,
                rule_value,
                rule_name,
                description,
                expires_at,
                disabled_details,
            ),
        ).json()

    def search(
        self,
        resource_type: list[str] | None = None,
        filter: dict[str, Any] | None = None,
        limit: int = 100,
        sort: list[str] | None = None,
        next: str | None = None,
    ) -> dict[str, Any]:
        """Search recast rules using the API's search endpoint.

        Args:
            resource_type (list, optional): Resource types to search. Each must
                be ``HOST``, ``HOST_AUDIT``, or ``WEBAPP``.
            filter (dict, optional): API-defined search filter.
            limit (int, optional): Maximum rules to request, from 1 to 500.
                Defaults to 100.
            sort (list, optional): API-defined sort expressions.
            next (str, optional): Pagination cursor from an earlier response.

        Returns:
            dict: The search response, including any pagination data supplied
            by the API.

        Examples:
            Request up to 25 host rules:

            >>> tio.recast_rules.search(resource_type=['HOST'], limit=25)
        """
        limit = self._check('limit', limit, int)
        if not 1 <= limit <= 500:
            raise ValueError('limit must be between 1 and 500')

        payload: dict[str, Any] = {'limit': limit}
        if resource_type is not None:
            resource_type = self._check('resource_type', resource_type, list)
            payload['resource_type'] = [
                self._check('resource_type', item, str, choices=self._resource_types)
                for item in resource_type
            ]
        if filter is not None:
            payload['filter'] = self._check('filter', filter, dict)
        if sort is not None:
            payload['sort'] = self._check('sort', sort, list)
        if next is not None:
            payload['next'] = self._check('next', next, str)

        return self._api.post('v1/recast/rules/search', json=payload).json()

    def details(self, rule_id: str) -> dict[str, Any]:
        """Retrieve a recast rule by UUID.

        Args:
            rule_id (str): UUID of the rule to retrieve.

        Returns:
            dict: The rule response from the API.

        Examples:
            >>> tio.recast_rules.details('4c931fce-699c-4052-a43c-c953e71dd37b')
        """
        return self._api.get(f'v1/recast/rules/{scrub(self._check("rule_id", rule_id, "uuid"))}').json()

    def edit(
        self,
        rule_id: str,
        resource_type: str,
        rule_value: dict[str, Any],
        rule_name: str | None = None,
        description: str | None = None,
        expires_at: str | None = None,
        disabled_details: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Update a recast rule by UUID.

        Args:
            rule_id (str): UUID of the rule to update.
            resource_type (str): One of ``HOST``, ``HOST_AUDIT``, or ``WEBAPP``.
            rule_value (dict): Rule criteria accepted by the Recast Rules API.
            rule_name (str, optional): Name for the rule.
            description (str, optional): Description of the rule.
            expires_at (str, optional): Expiration timestamp accepted by the API.
            disabled_details (dict, optional): API-defined disabled-rule details.

        Returns:
            dict: The updated rule response from the API.

        Examples:
            >>> tio.recast_rules.edit(
            ...     '4c931fce-699c-4052-a43c-c953e71dd37b', 'HOST', rule_value
            ... )
        """
        return self._api.put(
            f'v1/recast/rules/{scrub(self._check("rule_id", rule_id, "uuid"))}',
            json=self._payload(
                resource_type,
                rule_value,
                rule_name,
                description,
                expires_at,
                disabled_details,
            ),
        ).json()

    def delete(self, rule_id: str) -> dict[str, Any]:
        """Delete a recast rule by UUID.

        Args:
            rule_id (str): UUID of the rule to delete.

        Returns:
            dict: The deletion response from the API.

        Examples:
            >>> tio.recast_rules.delete('4c931fce-699c-4052-a43c-c953e71dd37b')
        """
        return self._api.delete(
            f'v1/recast/rules/{scrub(self._check("rule_id", rule_id, "uuid"))}'
        ).json()

    def filters(self) -> dict[str, Any]:
        """Retrieve the filters available for recast rule searches.

        Returns:
            dict: The filter definitions returned by the API.

        Examples:
            >>> tio.recast_rules.filters()
        """
        return self._api.get('v1/recast/rules/filters').json()
