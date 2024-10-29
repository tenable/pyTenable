import logging
from typing import TYPE_CHECKING, Any

from pydantic import (
    BaseModel as PydanticBaseModel,
)
from pydantic import (
    ConfigDict,
    Field,
    StringConstraints,
    ValidationError,
    WrapValidator,
    model_validator,
)
from restfly.utils import trunc
from typing_extensions import Annotated

if TYPE_CHECKING:
    from pydantic_core.core_schema import ValidationInfo, ValidatorFunctionWrapHandler

logger = logging.getLogger('tenable.io.sync.schema')


def trunc_str(v: Any, handler: 'ValidatorFunctionWrapHandler', info: 'ValidationInfo'):
    """
    Ensure that a constrained string does not extend bewond the length limit.

    Args:
        v: The raw value of the constrained string
        handler: The upstream validator function
        info: The information about the field and the validator
    """
    try:
        return handler(v)
    except ValidationError as err:
        errors = err.errors()
        if len(errors) > 1 or errors[0]['type'] != 'string_too_long':
            raise err
        model = info.config['title']
        name = info.field_name
        limit = errors[0]['ctx']['max_length']
        value = trunc(v, limit)
        logger.warning(
            f'{model}.{name} has been truncated to {limit} chars, originally {len(str(v))}',
            SyntaxWarning,
        )
        return value


intpos = Annotated[int, Field(gt=0)]
int100 = Annotated[int, Field(gt=0, le=100)]
float100 = Annotated[float, Field(gt=0, le=100)]
str16 = Annotated[str, StringConstraints(max_length=16), WrapValidator(trunc_str)]
str32 = Annotated[str, StringConstraints(max_length=32), WrapValidator(trunc_str)]
str64 = Annotated[str, StringConstraints(max_length=64), WrapValidator(trunc_str)]
str128 = Annotated[str, StringConstraints(max_length=128), WrapValidator(trunc_str)]
str256 = Annotated[str, StringConstraints(max_length=256), WrapValidator(trunc_str)]
str512 = Annotated[str, StringConstraints(max_length=512), WrapValidator(trunc_str)]


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
    value: str512 | None


class ProductCPE(BaseModel):
    model_config = ConfigDict(str_to_lower=True)
    cpe: str512 | None = None
    product_name: str32 | None = None
    vendor_name: str32 | None = None
    version: str32 | None = None
