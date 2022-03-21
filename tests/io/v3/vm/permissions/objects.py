NEGATIVE_PERMISSION_ACL_SCHEMA = [
    {'invalid': 'key'},
    {'type': 123},
    {'type': 'invalid'},
    {'id': 'invalid'},
    {'permissions': False},
]

NEGATIVE_PERMISSION_SCHEMA = [
    {'invalid': 'key'},
    {'acls': 'invalid'},
    {'acls': ['invalid']},
    {'acls': [{'invalid': 'key'}]}
]
