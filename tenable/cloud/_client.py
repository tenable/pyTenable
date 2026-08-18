import os
import warnings
from ssl import SSLContext

from restfly import APIClient, AsyncAPIClient
from restfly.types import CertTypes, ProxyTypes

from ..errors import TenableCloudAPIError
from ..version import lib_name, version
from .platform import AsyncPlatformAPIs, PlatformAPIs

# TODO: We will eventually need to remove this when the new package is in a better
#       state.  This will likely take some time, and require the documentation wiring
#       to be performed as well.
warnings.warn(
    "The Tenable Cloud package is under very active development and may change over time.",
    Warning,
    stacklevel=1,
)


class TenableCloud(APIClient):
    _base_url = "https://cloud.tenable.com"
    _error_class = TenableCloudAPIError
    _lib_name = lib_name
    _lib_version = version
    _json_dump_kwargs = {"exclude_none": True}

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
    _json_dump_kwargs = {"exclude_none": True}

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
