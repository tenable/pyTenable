import os

import pytest

from tenable.cloud import AsyncTenableCloud, TenableCloud


def test_client_sync(httpx_mock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/test",
        match_headers={"X-ApiKeys": "accessKey=ABC;secretKey=DEF"},
    )
    client = TenableCloud(access_key="ABC", secret_key="DEF")
    client._get("/test")


def test_client_envvars(monkeypatch, httpx_mock):
    monkeypatch.setattr(
        os,
        "environ",
        {"TENABLE_CLOUD_ACCESS_KEY": "ABC", "TENABLE_CLOUD_SECRET_KEY": "DEF"},
    )

    httpx_mock.add_response(
        url="https://cloud.tenable.com/test",
        match_headers={"X-ApiKeys": "accessKey=ABC;secretKey=DEF"},
    )
    client = TenableCloud()
    client._get("/test")


def test_client_envvars_valueerror(monkeypatch):
    monkeypatch.setattr(os, "environ", {"TENABLE_CLOUD_ACCESS_KEY": "something"})
    with pytest.raises(ValueError):
        TenableCloud()


def test_client_envvars_url(monkeypatch, httpx_mock):

    httpx_mock.add_response(
        url="https://something.com/test",
        match_headers={"X-ApiKeys": "accessKey=ABC;secretKey=DEF"},
    )
    monkeypatch.setattr(os, "environ", {"TENABLE_CLOUD_URL": "https://something.com"})
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    cloud._get("/test")


@pytest.mark.asyncio
async def test_client_async(httpx_mock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/test",
        match_headers={"X-ApiKeys": "accessKey=ABC;secretKey=DEF"},
    )
    client = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    await client._get("/test")


@pytest.mark.asyncio
async def test_client_async_envvars(monkeypatch, httpx_mock):
    monkeypatch.setattr(
        os,
        "environ",
        {"TENABLE_CLOUD_ACCESS_KEY": "ABC", "TENABLE_CLOUD_SECRET_KEY": "DEF"},
    )

    httpx_mock.add_response(
        url="https://cloud.tenable.com/test",
        match_headers={"X-ApiKeys": "accessKey=ABC;secretKey=DEF"},
    )
    client = AsyncTenableCloud()
    await client._get("/test")


@pytest.mark.asyncio
async def test_client_async_envvars_valueerror(monkeypatch):
    monkeypatch.setattr(os, "environ", {"TENABLE_CLOUD_ACCESS_KEY": "something"})
    with pytest.raises(ValueError):
        AsyncTenableCloud()


@pytest.mark.asyncio
async def test_client_async_envvars_url(monkeypatch, httpx_mock):
    httpx_mock.add_response(
        url="https://something.com/test",
        match_headers={"X-ApiKeys": "accessKey=ABC;secretKey=DEF"},
    )
    monkeypatch.setattr(os, "environ", {"TENABLE_CLOUD_URL": "https://something.com"})
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    await cloud._get("/test")
