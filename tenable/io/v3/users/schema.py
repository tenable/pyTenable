'''
Users Endpoints Schema
'''
from marshmallow import Schema, fields


class UsersCreateSchema(Schema):
    '''
    Validate Create Users API Schema
    '''

    username = fields.Str()
    password = fields.Str()
    name = fields.Str()
    email = fields.Str()
    permissions = fields.Int()
    type = fields.Str(dump_default='local')


class UserEditSchema(Schema):
    '''
    Validate edit users API Schema
    '''

    permissions = fields.Int()
    name = fields.Str()
    email = fields.Email()
    enabled = fields.Boolean()


class UsersCommonSchema(Schema):
    '''
    Schema for common variables in users
    '''
    email_enabled = fields.Boolean()
    sms_enabled = fields.Boolean()
    sms_phone = fields.Str()
    password = fields.Str()
    current_password = fields.Str()
