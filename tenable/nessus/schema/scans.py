'''
Scan Export Schemas
'''
from marshmallow import Schema, fields, validate as v
from .pagination import FilterListSchema


class ReportContents(Schema):
    '''
    Additioinal options that can be used when exporting reports
    '''
    csv_columns = fields.Dict(data_key='csvColumns',
                              keys=fields.Str(validate=v.OneOf(['id',
                                           'cve',
                                           'cvss',
                                           'risk',
                                           'hostname',
                                           'protocol',
                                           'port',
                                           'plugin_name',
                                           'synopsis',
                                           'description',
                                           'solution',
                                           'see_also',
                                           'plugin_output',
                                           'stig_severity',
                                           'cvss4_base_score',
                                           'cvss4_bt_score',
                                           'cvss3_base_score',
                                           'cvss_temporal_score',
                                           'cvss3_temporal_score',
                                           'vpr_score',
                                           'epss_score',
                                           'risk_factor',
                                           'references',
                                           'plugin_information',
                                           'exploitable_with',
                                           ])),
                              values=fields.Bool(),
                              allow_none=True,
                              )

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
    report_contents = fields.Nested(ReportContents,
                                    data_key='reportContents',
                                    allow_none=True,
                                    )
    template_id = fields.Int(allow_none=True)
