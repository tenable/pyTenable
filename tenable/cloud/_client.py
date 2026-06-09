import os
from ssl import SSLContext

from restfly import APIClient, AsyncAPIClient
from restfly.types import CertTypes, ProxyTypes

from ..errors import TenableCloudAPIError
from ..version import lib_name, version
from .platform import AsyncPlatformAPIs, PlatformAPIs


class TenableCloud(APIClient):
    _base_url = "https://cloud.tenable.com"
    _error_class = TenableCloudAPIError
    _lib_name = lib_name
    _lib_version = version

    platform: PlatformAPIs

    def __init__(
        self,
        access_key: str | None = None,
        secret_key: str | None = None,
        url: str | None = None,
        proxy: ProxyTypes | None = None,
        verify: SSLContext | str | bool = True,
        cert: CertTypes | None = None,
        vendor: str = "unknown",
        product: str = "unknown",
        build: str = "unknown",
        retry_max: int = 5,
    ) -> None:
        """ """
        url = url if url is not None else os.getenv("TENABLE_CLOUD_URL")
        access_key = (
            access_key
            if access_key is not None
            else os.getenv("TENABLE_CLOUD_ACCESS_KEY")
        )
        secret_key = (
            secret_key
            if secret_key is not None
            else os.getenv("TENABLE_CLOUD_SECRET_KEY")
        )
        if access_key is None or secret_key is None:
            raise ValueError("API Keys required for use")

        super().__init__(
            base_url=url,
            proxy=proxy,
            verify=verify,
            cert=cert,
            vendor=vendor,
            product=product,
            build=build,
            retry_max=retry_max,
        )

        self._client.headers.update(
            {"X-ApiKeys": f"accessKey={access_key};secretKey={secret_key}"}
        )


class AsyncTenableCloud(AsyncAPIClient):
    _base_url = "https://cloud.tenable.com"
    _error_class = TenableCloudAPIError
    _lib_name = lib_name
    _lib_version = version

    platform: AsyncPlatformAPIs

    def __init__(
        self,
        access_key: str | None = None,
        secret_key: str | None = None,
        url: str | None = None,
        proxy: ProxyTypes | None = None,
        verify: SSLContext | str | bool = True,
        cert: CertTypes | None = None,
        vendor: str = "unknown",
        product: str = "unknown",
        build: str = "unknown",
        retry_max: int = 5,
    ) -> None:
        """ """
        url = url if url is not None else os.getenv("TENABLE_CLOUD_URL")
        access_key = (
            access_key
            if access_key is not None
            else os.getenv("TENABLE_CLOUD_ACCESS_KEY")
        )
        secret_key = (
            secret_key
            if secret_key is not None
            else os.getenv("TENABLE_CLOUD_SECRET_KEY")
        )
        if access_key is None or secret_key is None:
            raise ValueError("API Keys required for use")

        super().__init__(
            base_url=url,
            proxy=proxy,
            verify=verify,
            cert=cert,
            vendor=vendor,
            product=product,
            build=build,
            retry_max=retry_max,
        )

        self._client.headers.update(
            {"X-ApiKeys": f"accessKey={access_key};secretKey={secret_key}"}
        )
