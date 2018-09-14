from dateutil.parser import parse as dateparse
import uuid, datetime, os, sys, pytest

def check(i, name, val_type, allow_none=False):
    assert name in i
    if not allow_none:
        assert i[name] != None

    if i[name] != None:
        if val_type == 'datetime':
            assert isinstance(dateparse(i[name]), datetime.datetime)
        elif val_type == 'uuid':
            assert isinstance(uuid.UUID(i[name]), uuid.UUID)
        else:
            assert isinstance(i[name], val_type)