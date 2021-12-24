from marshmallow import Schema, fields, validate


class ScanStatusSchema(Schema):
    requested_action = fields.Str(
        validate=validate.OneOf(['stop'], error='Value not supported'),
        default='stop'
    )


class ScanReportSchema(Schema):
    content_type = fields.Str(
        allow_none=True,
        validate=validate.OneOf([
            'application/json',
            'application/pdf',
            'text/csv',
            'text/html',
            'text/xml'
        ]),
        default='application/json'
    )
