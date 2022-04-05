'''
Testing the Logos schemas
'''
from tenable.io.v3.mssp.logos.schema import LogoSchema


def test_schema():
    '''
    Validates schema for Logos API
    '''
    payload = {
        'account_ids': ['0fc4ef49-2649-4c76-bfa7-c181be3adf26'],
        'logo_id': 'a39f6b74-9b7f-4372-a7ac-a2a4bcb8dbad'
    }
    schema = LogoSchema()
    assert schema.load(schema.dump(payload)) == payload
