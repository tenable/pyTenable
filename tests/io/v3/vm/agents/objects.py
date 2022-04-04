NEGATIVE_CRITERIA_SCHEMA = [
    {'all_agents': 'string'},
    {'wildcard': 123},
    {'filters': 123},
    {'filters': [123]},
    {'filters': [False]},
    {'filter_type': 123},
    {'filter_type': 'invalid'},
    {'hardcoded_filters': 123},
    {'hardcoded_filters': False},
    {'hardcoded_filters': [123]},
    {'invalid': 'value'}
]

NEGATIVE_DIRECTIVE_SCHEMA = [
    {'invalid': 'key'},
    {'type': 123},
    {'type': True},
    {'type': 'invalid'},
    {'type': 'restart', 'invalid': 'key'},
    {'type': 'restart', 'option': 'invalid'},
]

NEGATIVE_AGENT_FILTER_SCHEMA = [
    {'_filters': 123},
    {'_filters': True},
    {'invalid': 'key'}
]

NEGATIVE_AGENT_SCHEMA = [
    {'filters': 'invalid'},
    {'filters': ['invalid']},
    {'filters': [True]},
    {'filters': [{'invalid': 'key'}]},
    {'invalid': 'key'},
    {'wildcard': 123},
    {'filter_type': 123},
    {'filter_type': 'invalid'},
    {'wildcard_fields': 'invalid'},
    {'wildcard_fields': [123]},
    {'sort': 'invalid'},
    {'sort': ['invalid']},
    {'sort': [(123, 123)]},
    {'sort': [('string', '123')]},
    {'sort': [()]},
    {'sort': [('invalid')]},
    {'limit': 'invalid'},
    {'offset': 'invalid'},
    {'items': 'invalid'},
    {'items': ['invalid']},
    {'not_items': ['invalid']},
    {'not_items': 'invalid'},
    {'criteria': 'invalid'},
    {'criteria': {'invalid': 'key'}},
    {'directive': {'invalid': 'key'}},
    {'directive': 'invalid'},
    {'directive': False},
]
