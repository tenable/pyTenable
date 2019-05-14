from dateutil.parser import parse as dateparse
import datetime, sys, re


def check(i, name, val_type, allow_none=False):
    assert name in i
    if not allow_none:
        assert i[name] != None
    single(i[name], val_type)


def single(var, val_type):
    reuuid = r'^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$'
    reuuids = r'^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12,32}$'

    if var != None:
        if val_type == 'datetime':
            assert isinstance(dateparse(var), datetime.datetime)
        elif val_type == 'uuid':
            assert len(re.findall(reuuid, var)) > 0
        elif val_type == 'scanner-uuid':
            assert len(re.findall(reuuids, var)) > 0
        elif sys.version_info.major == 2 and val_type == str:
            assert isinstance(var, unicode) or isinstance(var, str)
        else:
            assert isinstance(var, val_type)