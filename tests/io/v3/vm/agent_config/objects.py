NEGATIVE_AUTO_LINK_SCHEMA = [
    {'enabled': 'str'},
    {'expiration': 'str'},
    {'invalid': 'str'},
]

NEGATIVE_AGENT_CONFIG_SCHEMA = [
    {'software_update': 'str'},
    {'invalid': 'str'},
    {'auto_unlink': 'str'},
    {'auto_unlink': ['invalid']},
    {'auto_unlink': [{'enabled': 'invalid'}]},
]
