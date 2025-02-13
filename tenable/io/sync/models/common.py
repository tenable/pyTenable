import logging
import warnings
from typing import TYPE_CHECKING, Any

from pydantic import (
    AfterValidator,
    BeforeValidator,
    ConfigDict,
    Field,
    StringConstraints,
    ValidationError,
    WrapValidator,
    model_validator,
)
from pydantic import (
    BaseModel as PydanticBaseModel,
)
from restfly.utils import trunc
from typing_extensions import Annotated

if TYPE_CHECKING:
    from pydantic_core.core_schema import ValidationInfo, ValidatorFunctionWrapHandler

logger = logging.getLogger('tenable.io.sync.schema')


def trunc_str(
    v: Any, handler: 'ValidatorFunctionWrapHandler', info: 'ValidationInfo'
) -> str:
    """
    Ensure that a constrained string does not extend beyond the length limit.

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
        warnings.warn(
            f'{model}.{name} has been truncated to {limit} chars, originally {len(str(v))}',
            SyntaxWarning,
            stacklevel=0,
        )
        return value


def trunc_list(
    v: Any, handler: 'ValidatorFunctionWrapHandler', info: 'ValidationInfo'
) -> list:
    """
    Ensure that a constrained list does not extend beyond the length limit.  Please
    note that we are only truncating when a list extends beyond the max length, and
    will not do anything for a list that does not meet the minimum length.
    """
    try:
        return handler(v)
    except ValidationError as err:
        errors = err.errors()
        if len(errors) > 1 or errors[0]['type'] != 'too_long':
            raise err
        model = info.config['title']
        name = info.field_name
        limit = errors[0]['ctx']['max_length']
        value = v[:limit]
        warnings.warn(
            f'{model}.{name} has been truncated to {limit} items, originally {len(v)}',
            SyntaxWarning,
            stacklevel=0,
        )
        return value


def upper_if_exist(value: Any, default=None) -> Any:
    """
    Uppercase the string value if it exists and is a string
    """
    if value:
        return str(value).upper()
    if not value and default:
        return str(default).upper()
    return value


UpperCaseStr = BeforeValidator(lambda v: str(v).upper() if v else None)
UniqueList = AfterValidator(lambda v: list(set(v)) if v and len(v) > 0 else None)
TruncListValidator = WrapValidator(trunc_list)

intpos = Annotated[int, Field(gt=0)]
int100 = Annotated[int, Field(gt=0, le=100)]
int64k = Annotated[int, Field(ge=0, le=65535)]
float1000 = Annotated[int, Field(gt=0, le=1000)]
float100 = Annotated[float, Field(gt=0, le=100)]
floatpos = Annotated[float, Field(gt=0)]
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

    def __hash__(self) -> int:
        return hash(f'{self.name}:{str(self.value)}')

    def __eq__(self, other: Any) -> bool:
        return self.name == other.name and self.value == other.value


class ProductCPE(BaseModel):
    model_config = ConfigDict(str_to_lower=True)
    cpe: str512 | None = None
    product_name: str32 | None = None
    vendor_name: str32 | None = None
    version: str32 | None = None
