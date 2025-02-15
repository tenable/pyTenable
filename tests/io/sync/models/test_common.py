from typing import Annotated

import pytest
from pydantic import BaseModel, ValidationError

from tenable.io.sync.models import common


def test_string_truncation():
    # NOTE: As all of the annotated string lengths work the same way, we will only
    #       bother to test str16 and assume that all the rest will work as they are
    #       all identical aside from the length.s
    class M(BaseModel):
        x: common.str16

    assert M(x='this is a long string').model_dump() == {'x': 'this is a lon...'}

    # Any other errors are passed through and raised like you'd expect.
    with pytest.raises(ValidationError):
        M(x=False)


def test_base_model_empty_to_None():
    class M(common.BaseModel):
        x: int | None = None
        y: int | None = None
        z: int | None = None

    class N(M):
        a: list[int] | None = None

    assert N(y=1, a=[]).model_dump() == {'x': None, 'y': 1, 'z': None, 'a': None}
    assert M(y=1).model_dump() == {'x': None, 'y': 1, 'z': None}


def test_upper_if_exist():
    assert common.upper_if_exist(None) is None
    assert common.upper_if_exist('value') == 'VALUE'
    assert common.upper_if_exist(None, default='something') == 'SOMETHING'


def test_custom_attr_is_comparable():
    assert common.CustomAttribute(name='name', value='value') == common.CustomAttribute(
        name='name', value='value'
    )
    v = hash(common.CustomAttribute(name='name', value='value'))
    assert hash(common.CustomAttribute(name='name', value='value')) == v


def test_unique_list():
    class M(common.BaseModel):
        a: Annotated[list[int] | None, common.UniqueList]

    assert M(a=[1, 1, 2, 3]).model_dump() == {'a': [1, 2, 3]}
    assert M(a=[]).model_dump(exclude_none=True) == {}
    assert M(a=None).model_dump(exclude_none=True) == {}
