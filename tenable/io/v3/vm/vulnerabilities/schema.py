'''
VM Vulnerability API Endpoint Schemas
'''
from marshmallow import Schema, fields, validate


class VulnerabilityObjectSchema(Schema):
    '''
    Schema to validate vulnerabilities object in Assets
    '''
    tenable_plugin_id = fields.Str(required=True)
    cve = fields.Str()
    port = fields.Int()
    protocol = fields.Str()
    authenticated = fields.Bool()
    last_found = fields.Int()
    output = fields.Str()


class NetworkInterfaceObjectSchema(Schema):
    '''
    Schema to validate network_interface object in Assets
    '''
    ipv4 = fields.List(fields.Str())
    ipv6 = fields.List(fields.Str())
    mac_address = fields.Str()
    netbios_name = fields.Str()
    fqdn = fields.Str()


class AssetObjectSchema(Schema):
    '''
    Schema to validate Asset object in Payload
    '''
    network_interfaces = fields.List(
        fields.Nested(NetworkInterfaceObjectSchema)
    )
    hostname = fields.Str(required=True)
    servicenow_sysid = fields.Str()
    ssh_fingerprint = fields.Str()
    bios_uuid = fields.Str()
    netbios_name = fields.Str(required=True)
    operating_systems = fields.Str()
    tenable_agent_id = fields.Str()
    tenable_network_id = fields.Str()
    authenticated = fields.Bool()
    vulnerabilities = fields.List(
        fields.Nested(VulnerabilityObjectSchema)
    )


class VulnerabilitySchema(Schema):
    '''
    Schema to validate Vulnerabilities API
    '''
    vendor = fields.Str(required=True)
    data_type = fields.Str(required=True,
                           validate=validate.OneOf(['vm', 'was']))
    source = fields.Str(required=True)
    assets = fields.List(fields.Nested(AssetObjectSchema, required=True))
    product = fields.Str()
    coverage = fields.Str()
