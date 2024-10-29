from ipaddress import IPv4Address, IPv6Address
from typing import List, Literal, Optional

from pydantic import (
    AwareDatetime,
    BaseModel,
    Field,
    StringConstraints,
)
from pydantic_extra_types.mac_address import MacAddress
from typing_extensions import Annotated

from .common import (
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
    build_number: Optional[intpos] = None
    id: Optional[str] = None
    manufacturer: Optional[str64] = None
    version: Optional[str32] = None


class DeviceCPU(BaseModel):
    count: Optional[intpos] = None
    manufacturer: Optional[str64] = None
    name: Optional[str128] = None
    signature: Optional[str256] = None
    type: Optional[str64] = None


class DeviceHardware(BaseModel):
    bios: Optional[DeviceBios] = None
    cpu: Optional[DeviceCPU] = None
    family: Optional[str64] = None
    firmware: Optional[str64] = None
    manufacturer: Optional[str64] = None
    model: Optional[str64] = None
    ram_mb: Optional[intpos] = None
    serial_number: Optional[str64] = None
    tpm_id: Optional[str128] = None


class DeviceFQDN(BaseModel):
    type: Optional[Literal['REVERSE_LOOKUP', 'FORWARD_LOOKUP']] = None
    value: str256


class DeviceDHCPAssignment(BaseModel):
    lease_expires_at: Optional[AwareDatetime] = None
    lease_started_at: Optional[AwareDatetime] = None
    subnet_prefix: Optional[intpos] = None
    type: Literal['DHCP_STATIC', 'DHCP_DYNAMIC', 'MANUAL', 'APIPA', 'PPPOE']


class DeviceIPv6(BaseModel):
    address: Optional[IPv6Address] = None
    assignment: Optional[DeviceDHCPAssignment] = None


class DeviceIPv4(BaseModel):
    address: Optional[IPv4Address] = None
    assignment: Optional[DeviceDHCPAssignment] = None


class DeviceNetworking(BaseModel):
    fqdns: Optional[List[DeviceFQDN]] = None
    ip_address_v4: Optional[List[DeviceIPv4]] = None
    ip_address_v6: Optional[List[DeviceIPv6]] = None
    mac_addresses: Optional[List[MacAddress]] = None
    network_group_id: Optional[str64] = None


class DeviceOSServicePack(BaseModel):
    name: Optional[str64] = None
    version: Optional[intpos] = None


class DeviceOS(BaseModel):
    build: Optional[str64] = None
    confidence: Optional[int100] = None
    hoxfix: Optional[str64] = None
    product: Optional[ProductCPE] = None
    service_path: Optional[DeviceOSServicePack] = None
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
    hardware: Optional[DeviceHardware] = None
    manufacturer: Optional[str64] = None
    netbios_name: Optional[str16] = None
    networking: Optional[DeviceNetworking] = None
    operating_system: Optional[DeviceOS] = None
    status: Optional[
        Literal[
            'INITIALIZING',
            'RUNNING',
            'STOPPED',
            'TERMINATED',
            'FAULT',
        ]
    ] = None
    system_type: Optional[str32] = None
    uptime_ms: Optional[intpos] = None


class DeviceDiscoveryAuth(BaseModel):
    attempted: bool
    successful: bool
    type: Optional[Literal['AGENT', 'PASSIVE', 'AUTHENTICATED_SCAN', 'OTHER']] = None


class DeviceDiscovery(BaseModel):
    authentication: Optional[DeviceDiscoveryAuth] = None
    first_observed_at: Optional[AwareDatetime] = None
    last_observed_on: Optional[AwareDatetime] = None
    id: Optional[str64] = None
    produced_findings: Optional[bool] = None


class DeviceExternalId(BaseModel):
    qualifier: Optional[str32] = None
    value: Optional[str256] = None


class DeviceLifetime(BaseModel):
    delete_on: Optional[AwareDatetime] = None
    license_expires_at: Optional[AwareDatetime] = None
    type: Literal['UNTIL_DELETED', 'DELETE_AFTER']


class AssetTag(BaseModel):
    name: str128
    value: Optional[str512] = None


class AssetExposureCriticality(BaseModel):
    level: Literal['NONE', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
    score: Optional[float100] = None


class AssetExposure(BaseModel):
    criticality: Optional[AssetExposureCriticality] = None


class AssetLocationCity(BaseModel):
    name: str64
    postal_code: Optional[int] = None


class AssetLocationCountry(BaseModel):
    iso_code: Annotated[str, StringConstraints(max_length=3)]
    name: Optional[str64] = None


class AssetLocationGeo(BaseModel):
    latitude: Annotated[Optional[float], Field(le=-90, ge=90)] = None
    longitude: Annotated[Optional[float], Field(le=-180, ge=180)] = None


class AssetLocationStateOrProvince(BaseModel):
    name: str64
    abbreviation: Optional[str16] = None


class AssetLocation(BaseModel):
    area: Optional[str32] = None
    building: Optional[str64] = None
    city: Optional[AssetLocationCity] = None
    country: Optional[AssetLocationCountry] = None
    floor: Optional[str16] = None
    gro: Optional[AssetLocationGeo] = None
    network_drop_id: Optional[str64] = None
    state_or_province: Optional[AssetLocationStateOrProvince] = None


class DeviceAsset(BaseModel):
    object_type: Literal['device-asset'] = 'device-asset'
    asset_class: Literal['DEVICE'] = 'DEVICE'
    custom_attributes: Optional[List[CustomAttribute]] = None
    device: Device
    description: Optional[str512] = None
    discovery: Optional[DeviceDiscovery] = None
    external_ids: Optional[List[DeviceExternalId]] = None
    id: str128
    labels: Optional[List[str]] = None
    lifetime: Optional[DeviceLifetime] = None
    name: Optional[str128] = None
    tags: Optional[List[AssetTag]] = None
    exposure: Optional[AssetExposure] = None
    location: Optional[AssetLocation] = None
