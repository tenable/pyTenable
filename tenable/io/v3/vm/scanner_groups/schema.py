'''
Scanner-groups API Endpoint Schemas
'''

from marshmallow import Schema, fields
from marshmallow import validate as v


class ScannerGroupSchema(Schema):
    name = fields.Str()
    type = fields.Str(validate=v.OneOf(['load_balancing']))
    routes = fields.List(fields.Str())
