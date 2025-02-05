from typing import List

from pydantic import BaseModel, Field
from typing_extensions import Annotated

from .cve_finding import CVEFinding
from .device_asset import DeviceAsset

Object = Annotated[CVEFinding | DeviceAsset, Field(discriminator='object_type')]


class SyncChunkObjects(BaseModel):
    objects: List[Object]
