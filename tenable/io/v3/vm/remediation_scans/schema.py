'''
Schema for remediation scans endpoint
'''
from marshmallow import INCLUDE, Schema, fields, post_dump, validates


class RemScansDocumentCreateSchema(Schema):

    class Meta:
        unknown = INCLUDE

    name = fields.Str()
    template = fields.Str()
    scanner = fields.Str()
    targets = fields.List(fields.Str())
    credentials = fields.Dict()
    compliance = fields.Dict()
    enabled_plugins = fields.List(fields.Int())

    @validates('template')
    def validate_template(self, value):
        if self.context.get('templates_choices'):
            if value not in self.context['templates_choices']:
                raise ValueError('Template does not matches with choices')

    @validates('scanner')
    def validate_scanner(self, value):
        if self.context.get('scanners_choices'):
            if value not in self.context['scanners_choices']:
                raise ValueError('Scanner does not matches with choices')

    @post_dump(pass_original=True)
    def transform_data(self, data, org, **kwargs):
        if 'targets' in data:
            target_list = data.pop('targets')
            target_list = ','.join(target_list)
            data['targets'] = target_list

        for key in org:
            if key not in data:
                data[key] = org[key]
        return data
