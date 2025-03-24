from typing import Any

from pydantic import BaseModel, ConfigDict, model_validator


class BaseSchema(BaseModel):
    @model_validator(mode="before")
    def clean_strings(cls, values: Any) -> Any:
        return {k: v.strip() if isinstance(v, str) else v for k, v in values.items()}

    model_config = ConfigDict(from_attributes=True)
