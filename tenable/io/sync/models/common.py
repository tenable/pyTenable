from typing import Optional, Self

from pydantic import BaseModel, Field, StringConstraints, model_validator
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


class CustomAttribute(BaseModel):
    name: str128
    value: Optional[str512] = None


class ProductCPE(BaseModel):
    cpe: Optional[str512] = None
    product_name: Optional[str32] = None
    vendor_name: Optional[str32] = None
    version: Optional[str32] = None

    @model_validator(mode='after')
    def ensure_correct_fields_are_set(self) -> Self:
        if not self.cpe and not (self.product_name or self.vendor_name or self.version):
            raise ValueError(
                'product_name, vendor_name, and version must be set if cpe is not.'
            )
        return self
