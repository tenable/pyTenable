from typing import Any
from uuid import UUID

from pydantic import TypeAdapter
from restfly import APIEndpoint, AsyncAPIEndpoint

from tenable.utils import scrub

from .iterators import AsyncPaginationV1Iterator, PaginationV1Iterator
from .models.connectors import (
    Connector,
    ConnectorCFTTemplateRequest,
    ConnectorCFTTemplateResponse,
    ConnectorCloudtrailRequest,
    ConnectorCloudtrailResponse,
    ConnectorEnvelope,
    ConnectorListResponse,
    ConnectorParams,
    ConnectorQueryParams,
    ConnectorRegion,
    ConnectorRequest,
    ConnectorSchedule,
    ConnectorTrail,
    ConnectorUpdateResponse,
)


class ConnectorsIterator(PaginationV1Iterator):
    path: str
    page: list[Connector]
    params: ConnectorQueryParams
    _method = "platform.connectors._list_connectors"


class AsyncConnectorsIterator(AsyncPaginationV1Iterator):
    path: str
    page: list[Connector]
    params: ConnectorQueryParams
    _method = "platform.connectors._list_connectors"


class ConnectorsAPI(APIEndpoint):
    _path = "/settings/connectors"

    def _list_connectors(
        self, *, path: str, params: ConnectorQueryParams
    ) -> ConnectorListResponse:
        return self._client._get(
            path, params=params, response_model=ConnectorListResponse
        )

    def get(self, *, limit: int = 1000, sort: str | None = None) -> ConnectorsIterator:
        """
        Returns an iterator of cloud connectors.

        Args:
            limit: Number of records to retrieve per page. Defaults to ``1000``.
            sort:
                Sort expression, e.g. ``"name:desc"`` or
                ``"name:desc,date_created:asc"``.

        Returns:
            Iterator yielding connector objects.
        """
        params = ConnectorQueryParams.model_validate({"limit": limit, "sort": sort})
        return ConnectorsIterator(self._client, path=self._path, params=params)

    def details(self, connector_id: UUID | str) -> Connector:
        """
        Returns the details for the specified connector.

        Args:
            connector_id: The UUID of the connector to return details for.

        Returns:
            Requested connector object.
        """
        resp = self._get(f"/{scrub(connector_id)}", response_model=ConnectorEnvelope)
        return resp.connector

    def create(self, connector: ConnectorParams) -> Connector:
        """
        Creates a new cloud connector.

        Args:
            connector:
                The connector configuration to create, e.g. an
                :class:`~.models.connectors.AWSKeyedConnector` or
                :class:`~.models.connectors.AzureConnector` instance.

        Returns:
            The newly created connector.
        """
        resp: ConnectorEnvelope = self._post(
            json=ConnectorRequest.model_validate({"connector": connector}),
            response_model=ConnectorEnvelope,
        )
        return resp.connector

    def update(self, connector_id: UUID | str, *, connector: ConnectorParams) -> UUID:
        """
        Updates the specified connector. The connector type cannot be changed.

        Args:
            connector_id: The UUID of the connector to update.
            name: New name for the connector.
            network_uuid: New network UUID to associate with the connector.
            schedule: New data import schedule for the connector.
            params:
                Connector-type-specific parameters to overlay onto the connector's
                existing parameters. Note that secret values (e.g. ``secret_key``)
                are never returned by the API and must be resupplied here if they
                need to be retained.

        Returns:
            The UUID of the updated connector.
        """
        payload = TypeAdapter(ConnectorParams).validate_python(connector)
        resp: ConnectorUpdateResponse = self._put(
            f"/{scrub(connector_id)}",
            json=ConnectorRequest(connector=payload),
            response_model=ConnectorUpdateResponse,
        )
        return resp.id

    def delete(self, connector_id: UUID | str) -> None:
        """
        Deletes the specified connector.

        Args:
            connector_id: The UUID of the connector to delete.
        """
        self._delete(f"/{scrub(connector_id)}")

    def import_data(self, connector_id: UUID | str) -> Connector:
        """
        Schedules an asynchronous import of data using the specified connector.

        Args:
            connector_id: The UUID of the connector to import data with.

        Returns:
            The connector object, reflecting the scheduled import.
        """
        resp = self._post(
            f"/{scrub(connector_id)}/import", response_model=ConnectorEnvelope
        )
        return resp.connector

    def list_aws_cloudtrails(
        self,
        *,
        regions: list[str],
        access_key: str | None = None,
        secret_key: str | None = None,
        account_id: str | None = None,
    ) -> list[ConnectorTrail]:
        """
        Returns a list of available AWS Cloudtrails.

        Args:
            regions: The list of AWS regions to check for Cloudtrails.
            access_key: The AWS access key, for keyed connectors.
            secret_key: The AWS secret key, for keyed connectors.
            account_id: The AWS account ID, for keyless connectors.

        Returns:
            List of available cloudtrail objects.
        """
        req = ConnectorCloudtrailRequest.model_validate(
            {
                "region": [{"name": r} for r in regions],
                "credentials": {"access_key": access_key, "secret_key": secret_key},
                "account_id": account_id,
            }
        )
        resp: ConnectorCloudtrailResponse = self._post(
            "/aws/cloudtrails", json=req, response_model=ConnectorCloudtrailResponse
        )
        return resp.trails

    def cloudformation_template(
        self, connector_id: UUID | str, *, account_id: str
    ) -> ConnectorCFTTemplateResponse:
        """
        Returns a Cloud Formation Template (CFT) for AWS Frictionless Assessment
        connectors.

        Args:
            connector_id: The UUID of the connector to download a CFT template for.
            account_id: For keyless AWS connectors, the AWS account ID.

        Returns:
            The CFT template details.
        """
        req = ConnectorCFTTemplateRequest(
            connector_id=UUID(str(connector_id)), account_id=account_id
        )
        return self._post(
            "/cloudformation-template",
            json=req,
            response_model=ConnectorCFTTemplateResponse,
        )

    def arm_template(self, connector_id: UUID | str) -> dict[str, Any]:
        """
        Returns an Azure Resource Manager (ARM) template for Microsoft Azure
        Frictionless Assessment connectors.

        Args:
            connector_id: The UUID of the connector to download an ARM template for.

        Returns:
            The raw ARM template.
        """
        resp = self._get(f"/azure-fa/{scrub(connector_id)}/arm-template")
        return resp.json()


class AsyncConnectorsAPI(AsyncAPIEndpoint):
    _path = "/settings/connectors"

    async def _list_connectors(
        self, *, path: str, params: ConnectorQueryParams
    ) -> ConnectorListResponse:
        return await self._client._get(
            path, params=params, response_model=ConnectorListResponse
        )

    async def get(
        self, *, limit: int = 1000, sort: str | None = None
    ) -> AsyncConnectorsIterator:
        """
        Returns an async iterator of cloud connectors.

        Args:
            limit: Number of records to retrieve per page. Defaults to ``1000``.
            sort:
                Sort expression, e.g. ``"name:desc"`` or
                ``"name:desc,date_created:asc"``.

        Returns:
            Async iterator yielding connector objects.
        """
        params = ConnectorQueryParams.model_validate({"limit": limit, "sort": sort})
        return AsyncConnectorsIterator(self._client, path=self._path, params=params)

    async def details(self, connector_id: UUID | str) -> Connector:
        """
        Returns the details for the specified connector.

        Args:
            connector_id: The UUID of the connector to return details for.

        Returns:
            Requested connector object.
        """
        resp = await self._get(
            f"/{scrub(connector_id)}", response_model=ConnectorEnvelope
        )
        return resp.connector

    async def create(self, connector: ConnectorParams) -> Connector:
        """
        Creates a new cloud connector.

        Args:
            connector:
                The connector configuration to create, e.g. an
                :class:`~.models.connectors.AWSKeyedConnectorCreate` or
                :class:`~.models.connectors.AzureConnectorCreate` instance.

        Returns:
            The newly created connector.
        """
        resp: ConnectorEnvelope = await self._post(
            json=ConnectorRequest.model_validate({"connector": connector}),
            response_model=ConnectorEnvelope,
        )
        return resp.connector

    async def update(
        self, connector_id: UUID | str, *, connector: ConnectorParams
    ) -> UUID:
        """
        Updates the specified connector. The connector type cannot be changed.

        Args:
            connector_id: The UUID of the connector to update.
            name: New name for the connector.
            network_uuid: New network UUID to associate with the connector.
            schedule: New data import schedule for the connector.
            params:
                Connector-type-specific parameters to overlay onto the connector's
                existing parameters. Note that secret values (e.g. ``secret_key``)
                are never returned by the API and must be resupplied here if they
                need to be retained.

        Returns:
            The UUID of the updated connector.
        """
        payload = TypeAdapter(ConnectorParams).validate_python(connector)
        resp: ConnectorUpdateResponse = await self._put(
            f"/{scrub(connector_id)}",
            json=ConnectorRequest(connector=payload),
            response_model=ConnectorUpdateResponse,
        )
        return resp.id

    async def delete(self, connector_id: UUID | str) -> None:
        """
        Deletes the specified connector.

        Args:
            connector_id: The UUID of the connector to delete.
        """
        await self._delete(f"/{scrub(connector_id)}")

    async def import_data(self, connector_id: UUID | str) -> Connector:
        """
        Schedules an asynchronous import of data using the specified connector.

        Args:
            connector_id: The UUID of the connector to import data with.

        Returns:
            The connector object, reflecting the scheduled import.
        """
        resp = await self._post(
            f"/{scrub(connector_id)}/import", response_model=ConnectorEnvelope
        )
        return resp.connector

    async def list_aws_cloudtrails(
        self,
        *,
        regions: list[str],
        access_key: str | None = None,
        secret_key: str | None = None,
        account_id: str | None = None,
    ) -> list[ConnectorTrail]:
        """
        Returns a list of available AWS cloudtrails.

        Args:
            region: The list of AWS regions to check for cloudtrails.
            access_key: The AWS access key, for keyed connectors.
            secret_key: The AWS secret key, for keyed connectors.
            account_id: The AWS account ID, for keyless connectors.

        Returns:
            List of available cloudtrail objects.
        """
        req = ConnectorCloudtrailRequest.model_validate(
            {
                "region": [{"name": r} for r in regions],
                "credentials": {"access_key": access_key, "secret_key": secret_key},
                "account_id": account_id,
            }
        )
        resp: ConnectorCloudtrailResponse = await self._post(
            "/aws/cloudtrails", json=req, response_model=ConnectorCloudtrailResponse
        )
        return resp.trails

    async def cloudformation_template(
        self, connector_id: UUID | str, *, account_id: str
    ) -> ConnectorCFTTemplateResponse:
        """
        Returns a Cloud Formation Template (CFT) for AWS Frictionless Assessment
        connectors.

        Args:
            connector_id: The UUID of the connector to download a CFT template for.
            account_id: For keyless AWS connectors, the AWS account ID.

        Returns:
            The CFT template details.
        """
        req = ConnectorCFTTemplateRequest(
            connector_id=UUID(str(connector_id)), account_id=account_id
        )
        return await self._post(
            "/cloudformation-template",
            json=req,
            response_model=ConnectorCFTTemplateResponse,
        )

    async def arm_template(self, connector_id: UUID | str) -> dict[str, Any]:
        """
        Returns an Azure Resource Manager (ARM) template for Microsoft Azure
        Frictionless Assessment connectors.

        Args:
            connector_id: The UUID of the connector to download an ARM template for.

        Returns:
            The raw ARM template.
        """
        resp = await self._get(f"/azure-fa/{scrub(connector_id)}/arm-template")
        return resp.json()
