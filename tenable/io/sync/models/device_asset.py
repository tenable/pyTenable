from __future__ import annotations

from datetime import datetime
from ipaddress import IPv4Address, IPv6Address
from typing import Literal

from arrow import ArrowFactory
from pydantic import (
    AfterValidator,
    AwareDatetime,
    BeforeValidator,
    Field,
    PlainSerializer,
    StringConstraints,
)
from pydantic_extra_types.mac_address import MacAddress
from typing_extensions import Annotated

from .common import (
    BaseModel,
    CustomAttribute,
    ProductCPE,
    UniqueList,
    UpperCaseStr,
    float1000,
    int100,
    intpos,
    str16,
    str32,
    str64,
    str128,
    str256,
    str512,
)


def list_of_addresses(
    values: list['DeviceIPv6'] | list['DeviceIPv4'],
) -> list['DeviceIPv6'] | list['DeviceIPv4']:
    """
    Returns a list of unique device info objects that are not link local or loopback
    addresses.
    """
    resp = []
    for value in values:
        if (
            not (value.address.is_loopback or value.address.is_link_local)
            and value not in resp
        ):
            resp.append(value)
    if len(resp) > 0:
        return resp


NonLocalAddress = AfterValidator(list_of_addresses)


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
    type: (
        Annotated[
            Literal['REVERSE_LOOKUP', 'FORWARD_LOOKUP'],
            UpperCaseStr,
        ]
        | None
    ) = None
    value: str256

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other: 'DeviceFQDN') -> bool:
        return self.value == other.value


class DeviceDHCPAssignment(BaseModel):
    lease_expires_at: AwareDatetime | None = None
    lease_started_at: AwareDatetime | None = None
    subnet_prefix: intpos | None = None
    type: Annotated[
        Literal['DHCP_STATIC', 'DHCP_DYNAMIC', 'MANUAL', 'APIPA', 'PPPOE'],
        UpperCaseStr,
    ]


class DeviceIPv6(BaseModel):
    address: IPv6Address | None = None
    assignment: DeviceDHCPAssignment | None = None

    def __hash__(self):
        return hash(self.address)

    def __eq__(self, other: DeviceIPv6):
        return self.address == other.address


class DeviceIPv4(BaseModel):
    address: IPv4Address | None = None
    assignment: DeviceDHCPAssignment | None = None

    def __hash__(self):
        return hash(self.address)

    def __eq__(self, other: DeviceIPv4):
        return self.address == other.address


class DeviceNetworking(BaseModel):
    fqdns: Annotated[list[DeviceFQDN], UniqueList] | None = None
    ip_addresses_v4: Annotated[list[DeviceIPv4], NonLocalAddress] | None = None
    ip_addresses_v6: Annotated[list[DeviceIPv6], NonLocalAddress] | None = None
    mac_addresses: Annotated[list[MacAddress], UniqueList] | None = None
    network_group_id: str64 | None = None


class DeviceOSServicePack(BaseModel):
    name: str64 | None = None
    version: intpos | None = None


class DeviceOS(BaseModel):
    build: str64 | None = None
    confidence: int100 | None = None
    hotfix: str64 | None = None
    product: ProductCPE | None = None
    service_pack: DeviceOSServicePack | None = None
    type: Annotated[
        Literal[
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
        ],
        BeforeValidator(lambda v: str(v).upper() if v else 'UNKNOWN'),
        Field(default=None, validate_default=True),
    ] = 'UNKNOWN'


class Device(BaseModel):
    hardware: DeviceHardware | None = None
    manufacturer: str64 | None = None
    netbios_name: str16 | None = None
    networking: DeviceNetworking | None = None
    operating_system: DeviceOS | None = None
    status: (
        Annotated[
            Literal[
                'INITIALIZING',
                'RUNNING',
                'STOPPED',
                'TERMINATED',
                'FAULT',
            ],
            UpperCaseStr,
        ]
        | None
    ) = None
    system_type: str32 | None = None
    uptime_ms: intpos | None = None


class DeviceDiscoveryAuth(BaseModel):
    attempted: bool
    successful: bool
    type: (
        Annotated[
            Literal['AGENT', 'PASSIVE', 'AUTHENTICATED_SCAN', 'OTHER'],
            UpperCaseStr,
        ]
        | None
    ) = None


class DeviceDiscovery(BaseModel):
    authentication: DeviceDiscoveryAuth | None = None
    first_assessed_on: AwareDatetime | None = None
    last_assessed_on: AwareDatetime | None = None
    first_observed_on: AwareDatetime | None = None
    last_observed_on: AwareDatetime | None = None
    id: str64 | None = None
    assessment_status: Annotated[
        Literal['ATTEMPTED_FINDINGS', 'SKIPPED_FINDINGS'],
        UpperCaseStr,
    ]
    assessment_type: (
        Annotated[Literal['KEEP_ALIVE', 'INVENTORY', 'RISK_ASSESSMENT'], UpperCaseStr]
        | None
    ) = None


class DeviceExternalId(BaseModel):
    qualifier: Annotated[str32 | None, Field(pattern='^[a-z]([a-z0-9-]+\\.?)+$')] = None
    value: str256 | None = None

    def __hash__(self):
        return hash(f'{str(self.qualifier)}:{str(self.value)}')


class DeviceLifetime(BaseModel):
    delete_on: AwareDatetime | None = None
    license_expires_at: AwareDatetime | None = None
    type: Annotated[Literal['UNTIL_DELETED', 'DELETE_AFTER'], UpperCaseStr]


class AssetTag(BaseModel):
    name: str128
    value: str512 | None = None

    def __hash__(self):
        return hash(f'{self.name}:{str(self.value)}')


class AssetExposureCriticality(BaseModel):
    level: Annotated[
        Literal['NONE', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'],
        UpperCaseStr,
    ]
    score: float1000 | None = None


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
    scope: Annotated[Literal['GLOBAL', 'REGION', 'ZONE'], UpperCaseStr]
    zone_id: str32 | None = None


class AssetCloudNetworking(BaseModel):
    subnet_id: str128 | None = None
    virtual_network_id: str128 | None = None


class AssetCloudProvider(BaseModel):
    id: str128
    type: Annotated[Literal['AWS', 'GCP', 'AZURE', 'OTHER'], UpperCaseStr]


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
    custom_attributes: Annotated[list[CustomAttribute], UniqueList] | None = None
    device: Device
    description: str512 | None = None
    discovery: DeviceDiscovery | None = None
    external_ids: Annotated[list[DeviceExternalId], UniqueList] | None = None
    id: str128
    cloud: AssetCloud | None = None
    labels: Annotated[list[str], UniqueList] | None = None
    lifetime: DeviceLifetime | None = None
    name: str128 | None = None
    tags: Annotated[list[AssetTag], UniqueList] | None = None
    exposure: AssetExposure | None = None
    location: AssetLocation | None = None
