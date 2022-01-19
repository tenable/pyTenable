'''
Folders API Endpoint Schemas
'''
from marshmallow import Schema, fields


class FolderSchema(Schema):
    '''
    Schema for folders API
    '''
    name = fields.Str()
