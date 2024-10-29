from typing import Optional, Self

from pydantic import (
    BaseModel as PydanticBaseModel,
)
from pydantic import (
    ConfigDict,
    Field,
    StringConstraints,
    model_validator,
)
from typing_extensions import Annotated

intpos = Annotated[int, Field(gt=0)]
int100 = Annotated[int, Field(gt=0, le=100)]
float100 = Annotated[float, Field(gt=0, le=100)]
str16 = Annotated[str, StringConstraints(max_length=16)]
str32 = Annotated[str, StringConstraints(max_length=32)]
str64 = Annotated[str, StringConstraints(max_length=64)]
str128 = Annotated[str, StringConstraints(max_length=128)]
str256 = Annotated[str, StringConstraints(max_length=256)]
str512 = Annotated[str, StringConstraints(max_length=512)]


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(extra='forbid')

    @model_validator(mode='before')
    @classmethod
    def empty_list_to_none(cls, data):
        if isinstance(data, dict):
            return {k: None if v == [] else v for k, v in data.items()}
        return data


class CustomAttribute(BaseModel):
    name: str128
    value: Optional[str512] = None


class ProductCPE(BaseModel):
    model_config = ConfigDict(str_to_lower=True)
    cpe: Optional[str512] = None
    product_name: Optional[str32] = None
    vendor_name: Optional[str32] = None
    version: Optional[str32] = None
