'''
Testing the Permissions Schema
'''
import pytest
from marshmallow import ValidationError

from tenable.io.v3.vm.permissions.schema import (PermissionAclSchema,
                                                 PermissionSchema)
from tests.io.v3.vm.permissions.objects import (NEGATIVE_PERMISSION_ACL_SCHEMA,
                                                NEGATIVE_PERMISSION_SCHEMA)

permission_acl_schema = PermissionAclSchema()
permission_schema = PermissionSchema()


def test_schema():
    acls = {
        'acls': [{'type': 'user', 'id': 2236706, 'permissions': 64}]}
    assert permission_schema.dump(permission_schema.load(acls)) == acls


@pytest.mark.parametrize("test_input", NEGATIVE_PERMISSION_ACL_SCHEMA)
def test_permission_acl_schema_negative(test_input):
    with pytest.raises(ValidationError):
        permission_acl_schema.load(test_input)


@pytest.mark.parametrize("test_input", NEGATIVE_PERMISSION_SCHEMA)
def test_permission_schema_negative(test_input):
    with pytest.raises(ValidationError):
        permission_schema.load(test_input)
