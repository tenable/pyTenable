from io import BytesIO

import pytest
from pytest_httpx import HTTPXMock

from tenable.cloud import AsyncTenableCloud, TenableCloud
from tenable.errors import TenableCloudAPIError

UPLOAD_URL = "https://cloud.tenable.com/file/upload"


def _fobj(content: bytes = b"192.0.2.1\n192.0.2.2\n") -> BytesIO:
    fobj = BytesIO(content)
    fobj.name = "scan_targets.txt"
    return fobj


def _assert_upload(httpx_mock: HTTPXMock, content: bytes) -> None:
    request = httpx_mock.get_request()
    assert request is not None
    body = request.read()
    assert request.headers["Content-Type"].startswith("multipart/form-data")
    assert b'name="Filedata"; filename="scan_targets.txt"' in body
    assert content in body


def test_files_upload(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=UPLOAD_URL, method="post", json={"fileuploaded": "scan_targets.txt"}
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert cloud.platform.files.upload(_fobj()) == "scan_targets.txt"
    _assert_upload(httpx_mock, b"192.0.2.1\n192.0.2.2\n")


def test_files_upload_encrypted(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{UPLOAD_URL}?no_enc=1",
        method="post",
        json={"fileuploaded": "scan_targets_1.txt"},
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert cloud.platform.files.upload(_fobj(), encrypted=True) == "scan_targets_1.txt"


def test_files_upload_error(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url=UPLOAD_URL, method="post", status_code=403)
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    with pytest.raises(TenableCloudAPIError):
        cloud.platform.files.upload(_fobj())


@pytest.mark.asyncio
async def test_async_files_upload(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=UPLOAD_URL, method="post", json={"fileuploaded": "scan_targets.txt"}
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert await cloud.platform.files.upload(_fobj()) == "scan_targets.txt"
    _assert_upload(httpx_mock, b"192.0.2.1\n192.0.2.2\n")


@pytest.mark.asyncio
async def test_async_files_upload_encrypted(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{UPLOAD_URL}?no_enc=1",
        method="post",
        json={"fileuploaded": "scan_targets_1.txt"},
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    result = await cloud.platform.files.upload(_fobj(), encrypted=True)
    assert result == "scan_targets_1.txt"
