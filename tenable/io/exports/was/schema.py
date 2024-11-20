"""
WAS Export API Endpoints Schemas
"""
import enum

from marshmallow import Schema, fields, post_dump
from tenable.base.utils.envelope import envelope

from tenable.io.exports.schema import VPRSchema


class OWASPChapters(enum.StrEnum):
    """
    Enum of OWASP Chapters
    """
    A1 = "A1"
    A2 = "A2"
    A3 = "A3"
    A4 = "A4"
    A5 = "A5"
    A6 = "A6"
    A7 = "A7"
    A8 = "A8"
    A9 = "A9"
    A10 = "A10"


class OWASPAPIChapters(enum.StrEnum):
    """
    Enum of OWASP API Chapters.
    """
    API1 = "API1"
    API2 = "API2"
    API3 = "API3"
    API4 = "API4"
    API5 = "API5"
    API6 = "API6"
    API7 = "API7"
    API8 = "API8"
    API9 = "API9"
    API10 = "API10"


class Severity(enum.StrEnum):
    """
    Enum for Severity level
    """
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class State(enum.StrEnum):
    """
    Enum for Finding State
    """
    OPEN = "OPEN"
    REOPENED = "REOPENED"
    FIXED = "FIXED"


class SeverityModificationType(enum.StrEnum):
    """
    Enum for SeverityModificationType
    """
    NONE = "NONE"
    ACCEPTED = "ACCEPTED"
    RECASTED = "RECASTED"


class WASVulnExportSchema(Schema):
    """
    WAS vulns Export API Schema
    """
    # asset fields
    asset_uuid = fields.List(fields.UUID())
    asset_name = fields.Str()

    # Temporal fields
    first_found = fields.Int()
    last_found = fields.Int()
    last_fixed = fields.Int()
    indexed_at = fields.Int()
    since = fields.Int()

    # Plugin fields
    plugin_ids = fields.List(fields.Int())

    # OWASP fields
    owasp_2010 = fields.List(fields.Enum(OWASPChapters))
    owasp_2013 = fields.List(fields.Enum(OWASPChapters))
    owasp_2017 = fields.List(fields.Enum(OWASPChapters))
    owasp_2021 = fields.List(fields.Enum(OWASPChapters))
    owasp_api_2019 = fields.List(fields.Enum(OWASPAPIChapters))

    # Vulnerability Findings fields
    severity = fields.List(fields.Enum(Severity))
    state = fields.List(fields.Enum(State))
    severity_modification_type = fields.List(fields.Enum(SeverityModificationType))
    vpr_score = fields.Nested(VPRSchema())
    ipv4s = fields.List(fields.IPv4())

    include_unlicensed = fields.Bool(default=False)
    # Chunking fields
    num_assets = fields.Int(dump_default=50)

    @post_dump
    def post_serialization(self, data, **kwargs):  # noqa PLR0201 PLW0613
        data = envelope(data, 'filters', excludes=['num_assets',
                                                   'include_unlicensed'
                                                   ])
        return data

