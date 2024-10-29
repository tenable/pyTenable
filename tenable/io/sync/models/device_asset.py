from datetime import datetime
from ipaddress import IPv4Address, IPv6Address
from typing import Literal

from pydantic import (
    AwareDatetime,
    Field,
    StringConstraints,
)
from pydantic_extra_types.mac_address import MacAddress
from typing_extensions import Annotated

from .common import (
    BaseModel,
    CustomAttribute,
    ProductCPE,
    float100,
    int100,
    intpos,
    str16,
    str32,
    str64,
    str128,
    str256,
    str512,
)


class DeviceBios(BaseModel):
    build_number: intpos | None = None
    id: str | None = None
    manufacturer: Annotated[str64 | None, StringConstraints(to_lower=True)] = None
    version: str32 | None = None


class DeviceCPU(BaseModel):
    count: intpos | None = None
    manufacturer: Annotated[str64 | None, StringConstraints(to_lower=True)] = None
    name: str128 | None = None
    signature: str256 | None = None
    type: str64 | None = None


class DeviceHardware(BaseModel):
    bios: DeviceBios | None = None
    cpu: DeviceCPU | None = None
    family: str64 | None = None
    firmware: str64 | None = None
    manufacturer: str64 | None = None
    model: str64 | None = None
    ram_mb: intpos | None = None
    serial_number: str64 | None = None
    tpm_id: str128 | None = None


class DeviceFQDN(BaseModel):
    type: Literal['REVERSE_LOOKUP', 'FORWARD_LOOKUP'] | None = None
    value: str256


class DeviceDHCPAssignment(BaseModel):
    lease_expires_at: AwareDatetime | None = None
    lease_started_at: AwareDatetime | None = None
    subnet_prefix: intpos | None = None
    type: Literal['DHCP_STATIC', 'DHCP_DYNAMIC', 'MANUAL', 'APIPA', 'PPPOE']


class DeviceIPv6(BaseModel):
    address: IPv6Address | None = None
    assignment: DeviceDHCPAssignment | None = None


class DeviceIPv4(BaseModel):
    address: IPv4Address | None = None
    assignment: DeviceDHCPAssignment | None = None


class DeviceNetworking(BaseModel):
    fqdns: list[DeviceFQDN] | None = None
    ip_addresses_v4: list[DeviceIPv4] | None = None
    ip_addresses_v6: list[DeviceIPv6] | None = None
    mac_addresses: list[MacAddress] | None = None
    network_group_id: str64 | None = None


class DeviceOSServicePack(BaseModel):
    name: str64 | None = None
    version: intpos | None = None


class DeviceOS(BaseModel):
    build: str64 | None = None
    confidence: int100 | None = None
    hoxfix: str64 | None = None
    product: ProductCPE | None = None
    service_path: DeviceOSServicePack | None = None
    type: Literal[
        'UNKNOWN',
        'OTHER',
        'WINDOWS',
        'WINDOWS_MOBILE',
        'LINUX',
        'ANDROID',
        'MAC_OS',
        'IOS',
        'SOLARIS',
        'AIX',
        'HP_UX',
    ]


class Device(BaseModel):
    hardware: DeviceHardware | None = None
    manufacturer: str64 | None = None
    netbios_name: str16 | None = None
    networking: DeviceNetworking | None = None
    operating_system: DeviceOS | None = None
    status: (
        Literal[
            'INITIALIZING',
            'RUNNING',
            'STOPPED',
            'TERMINATED',
            'FAULT',
        ]
        | None
    ) = None
    system_type: str32 | None = None
    uptime_ms: intpos | None = None


class DeviceDiscoveryAuth(BaseModel):
    attempted: bool
    successful: bool
    type: Literal['AGENT', 'PASSIVE', 'AUTHENTICATED_SCAN', 'OTHER'] | None = None


class DeviceDiscovery(BaseModel):
    authentication: DeviceDiscoveryAuth | None = None
    first_observed_at: AwareDatetime | None = None
    last_observed_on: AwareDatetime | None = None
    id: str64 | None = None
    produced_findings: bool | None = None


class DeviceExternalId(BaseModel):
    qualifier: Annotated[str32 | None, Field(pattern='^[a-z]([a-z0-9-]+\\.?)+$')] = None
    value: str256 | None = None


class DeviceLifetime(BaseModel):
    delete_on: AwareDatetime | None = None
    license_expires_at: AwareDatetime | None = None
    type: Literal['UNTIL_DELETED', 'DELETE_AFTER']


class AssetTag(BaseModel):
    name: str128
    value: str512 | None = None


class AssetExposureCriticality(BaseModel):
    level: Literal['NONE', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
    score: float100 | None = None


class AssetExposure(BaseModel):
    criticality: AssetExposureCriticality | None = None


class AssetLocationCity(BaseModel):
    name: str64
    postal_code: int | None = None


class AssetLocationCountry(BaseModel):
    iso_code: Annotated[str, StringConstraints(max_length=3)]
    name: str64 | None = None


class AssetLocationGeo(BaseModel):
    latitude: Annotated[float | None, Field(le=-90, ge=90)] = None
    longitude: Annotated[float | None, Field(le=-180, ge=180)] = None


class AssetLocationStateOrProvince(BaseModel):
    name: str64
    abbreviation: Annotated[str16 | None, StringConstraints(to_upper=True)] = None


class AssetLocation(BaseModel):
    area: str32 | None = None
    building: str64 | None = None
    city: AssetLocationCity | None = None
    country: AssetLocationCountry | None = None
    floor: str16 | None = None
    gro: AssetLocationGeo | None = None
    network_drop_id: str64 | None = None
    state_or_province: AssetLocationStateOrProvince | None = None


class AssetCloudCompute(BaseModel):
    image_id: str128 | None = None
    terminated_at: datetime | None = None
    type: str32


class AssetCloudLocation(BaseModel):
    region_id: str16 | None = None
    scope: Literal['GLOBAL', 'REGION', 'ZONE']
    zone_id: str32 | None = None


class AssetCloudNetworking(BaseModel):
    subnet_id: str128 | None = None
    virtual_network_id: str128 | None = None


class AssetCloudProvider(BaseModel):
    id: str128
    type: Literal['AWS', 'GCP', 'AZURE', 'OTHER']


class AssetCloud(BaseModel):
    compute: AssetCloudCompute | None = None
    id: str256
    location: AssetCloudLocation | None = None
    name: str256
    networking: AssetCloudNetworking | None = None
    provider: AssetCloudProvider
    type: str128


class DeviceAsset(BaseModel):
    object_type: Literal['device-asset'] = 'device-asset'
    asset_class: Literal['DEVICE'] = 'DEVICE'
    custom_attributes: list[CustomAttribute] | None = None
    device: Device
    description: str512 | None = None
    discovery: DeviceDiscovery | None = None
    external_ids: list[DeviceExternalId] | None = None
    id: str128
    cloud: AssetCloud | None = None
    labels: list[str] | None = None
    lifetime: DeviceLifetime | None = None
    name: str128 | None = None
    tags: list[AssetTag] | None = None
    exposure: AssetExposure | None = None
    location: AssetLocation | None = None
