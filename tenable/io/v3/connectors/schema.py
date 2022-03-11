from marshmallow import Schema, ValidationError, fields, pre_load
from marshmallow import validate as v


class ConnectorSchedule(Schema):
    units = fields.Str()
    value = fields.Int()

    @pre_load
    def transform_data(self, data, **kwargs):
        if isinstance(data, tuple) and len(data) == 2:
            units = data[0]
            value = data[1]
            return dict(units=units, value=value)
        elif isinstance(data, dict) and len(data) == 2:
            return data
        else:
            raise ValidationError('Invalid Schedule definition')


class ConnectorCreateOrEditSchema(Schema):
    name = fields.Str()
    type = fields.Str()
    network_id = fields.UUID()
    params = fields.Dict(required=True)
    schedule = fields.Nested(ConnectorSchedule)


class ConnectorRegion(Schema):
    name = fields.Str()
    friendly_name = fields.Str()

    @pre_load(pass_many=True)
    def transform_data(self, data, **kwargs):
        if isinstance(data, tuple) and len(data) == 2:
            name = data[0]
            f_name = data[1]
            return dict(name=name, friendly_name=f_name)
        return data


class ConnectorListTrails(Schema):
    region = fields.List(fields.Nested(ConnectorRegion))
    credentials = fields.Dict(keys=fields.String(validate=v.OneOf(
        choices=['access_key', 'secret_key'])),
        values=fields.Str()
    )
    account_id = fields.Str()
