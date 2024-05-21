'''
Scan Export Schemas
'''
from marshmallow import fields, validate as v
from .pagination import FilterListSchema


class ScanExportSchema(FilterListSchema):
    '''
    Scan Export Schema
    '''

    format = fields.Str(validate=v.OneOf(['nessus',
                                          'html',
                                          'pdf',
                                          'csv',
                                          'db'
                                          ]),
                        load_default='nessus',
                        )
    password = fields.Str(allow_none=True)
    template_id = fields.Int(allow_none=True)
