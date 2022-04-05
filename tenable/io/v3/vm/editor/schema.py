from marshmallow import Schema, fields, validate


class EditorSchema(Schema):
    '''
    Schema for editor
    '''
    etype = fields.Str(
        required=True,
        validate=validate.OneOf(['scan', 'policy', 'scan/policy'])
    )


class EditorAuditSchema(Schema):
    '''
    Schema for audit file
    '''
    etype = fields.Str(
        required=True,
        validate=validate.OneOf(['scan', 'policy'])
    )


class EditorTemplateSchema(Schema):
    '''
    Schema for editor template
    '''
    etype = fields.Str(
        required=True,
        validate=validate.OneOf(['scan', 'policy', 'remediation'])
    )
