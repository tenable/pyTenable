from marshmallow import fields
from tenable.ie.base.schema import CamelCaseSchema


class TopologyDirectoriesSchema(CamelCaseSchema):
    uid = fields.Str()
    name = fields.Str()
    known = fields.Bool()
    id = fields.Int()


class TopologyInfrastructuresSchema(CamelCaseSchema):
    uid = fields.Str()
    name = fields.Str()
    known = fields.Bool()
    directories = fields.Nested(TopologyDirectoriesSchema, many=True)


class TopologyTrustsSchema(CamelCaseSchema):
    from_key = fields.Str(data_key='from')
    to = fields.Str()
    hazard_level = fields.Str()
    attributes = fields.List(fields.Str())


class TopologySchema(CamelCaseSchema):
    profile_id = fields.Str()
    infrastructures = fields.Nested(TopologyInfrastructuresSchema, many=True)
    trusts = fields.Nested(TopologyTrustsSchema, many=True)
