from dateutil.parser import parse as dateparse
import datetime, sys, re

def check(i, name, val_type, allow_none=False):
    reuuid = r'^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$'
    reuuids = r'^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12,32}$'
    assert name in i
    if not allow_none:
        assert i[name] != None

    if i[name] != None:
        if val_type == 'datetime':
            assert isinstance(dateparse(i[name]), datetime.datetime)
        elif val_type == 'uuid':
            assert len(re.findall(reuuid, i[name])) > 0
        elif val_type == 'scanner-uuid':
            assert len(re.findall(reuuids, i[name])) > 0
        elif sys.version_info.major == 2 and val_type == str:
            assert isinstance(i[name], unicode) or isinstance(i[name], str)
        else:
            assert isinstance(i[name], val_type)