'''
Users API Endpoints Schemas
'''
from marshmallow import Schema, fields


class UsersCreateSchema(Schema):
    '''
    Validate Create Users API Schema
    '''
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    name = fields.Str()
    email = fields.Str()
    permissions = fields.Int(required=True)
    type = fields.Str(default='local')


class UserEditSchema(Schema):
    '''
    Validate edit users API Schema
    '''
    permissions = fields.Int()
    name = fields.Str()
    email = fields.Email()
    enabled = fields.Boolean()
