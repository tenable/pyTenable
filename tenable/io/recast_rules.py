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
    """The Tenable Vulnerability Management Recast Rules API."""

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
        """Create a recast rule."""
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
        """Search recast rules."""
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
        """Retrieve a recast rule by UUID."""
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
        """Update a recast rule by UUID."""
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
        """Delete a recast rule by UUID."""
        return self._api.delete(
            f'v1/recast/rules/{scrub(self._check("rule_id", rule_id, "uuid"))}'
        ).json()

    def filters(self) -> dict[str, Any]:
        """Retrieve the available recast rule filters."""
        return self._api.get('v1/recast/rules/filters').json()
