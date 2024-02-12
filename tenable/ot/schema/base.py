import ipaddress
import uuid
from dataclasses import dataclass
from typing import List


@dataclass
class AssetInfo:
    id: uuid.UUID
    name: str


@dataclass
class NodesList:
    nodes: List[str]

    def __iter__(self):
        yield from self.nodes

    def __len__(self):
        return len(self.nodes)

    def __getitem__(self, index):
        return self.nodes[index]


@dataclass
class AssetInfo:
    id: uuid.UUID
    name: str


@dataclass
class AssetInfoList(NodesList):
    nodes: List[AssetInfo]


@dataclass
class IP:
    ip: ipaddress.IPv4Address


@dataclass
class IPList:
    nodes: List[IP]


@dataclass
class ID:
    id: uuid.UUID


@dataclass
class IDList:
    nodes: List[ID]
