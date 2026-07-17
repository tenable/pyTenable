import pytest
from pydantic import ValidationError

from tenable.cloud._common import BaseModel, Permission, Role, ser_role_str_to_int


class PermModel(BaseModel):
    perm: Permission


class RoleModel(BaseModel):
    role: Role


def test_permission_from_int():
    m = PermModel.model_validate({"perm": 64})
    assert m.perm == "can_edit"


def test_permission_from_string():
    m = PermModel.model_validate({"perm": "can_edit"})
    assert m.perm == "can_edit"


def test_permission_serialization():
    m = PermModel.model_validate({"perm": 64})
    assert m.model_dump() == {"perm": 64}


def test_permission_invalid_label_serializer():
    m = PermModel.model_construct(perm="invalid_perm")  # type: ignore[call-arg]
    with pytest.raises(ValueError, match="not a valid permission label"):
        m.model_dump()


def test_permission_invalid_int():
    with pytest.raises(ValidationError):
        PermModel.model_validate({"perm": 999})


def test_role_invalid_label_serializer():
    with pytest.raises(ValueError, match="not a valid role label"):
        ser_role_str_to_int("super_admin", lambda x: x)  # type: ignore[arg-type]


def test_role_invalid_int():
    with pytest.raises(ValidationError):
        RoleModel.model_validate({"role": 999})
