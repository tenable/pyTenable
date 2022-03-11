NEGATIVE_CRITERIA_SCHEMA = [
    {'all_agents': 'invalid'},
    {'invalid': 'key'},
    {'wildcard': 123},
    {'filters': 123},
    {'filters': [True]},
    {'filter_type': False},
    {'filter_type': 'invalid'},
    {'hardcoded_filters': 123},
    {'hardcoded_filters': [123]},
]

NEGATIVE_DIRECTIVE_SCHEMA = [
    {'invalid': 'key'},
    {'type': 123},
    {'type': 'invalid'},
    {'type': 'restart', 'option': 'invalid'},
    {'option': {}}
]

NEGATIVE_AGENT_GROUP_FILTER_SCHEMA = [
    {'invalid': 'key'}
]

NEGATIVE_AGENT_GROUP_SCHEMA = [
    {'invalid': 'key'},
    {'items': 'invalid'},
    {'items': ['invalid']},
    {'wildcard': 123},
    {'filter_type': True},
    {'filter_type': 'invalid'},
    {'wildcard_fields': 123},
    {'wildcard_fields': [123]},
    {'sort': True},
    {'sort': ['invalid']},
    {'sort': [(True, 'asc')]},
    {'sort': [('value', 123)]},
    {'sort': [('value', 'invalid')]},
    {'limit': 'invalid'},
    {'offset': 'invalid'},
    {'not_items': 'invalid'},
    {'not_items': ['invalid']},
    {'criteria': True},
    {'criteria': {'invalid': 'key'}},
    {'directive': {'invalid': 'key'}},
    {'directive': 123}
]
