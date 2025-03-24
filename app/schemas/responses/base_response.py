from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)
M = TypeVar("M", bound=BaseModel)

class EmptyDataResponse(BaseModel):
    pass

class EmptyMetaResponse(BaseModel):
    pass

class DetailResponse(BaseModel, Generic[T, M]):
    name: str = "OK"
    message: str = "Yêu cầu đã được xử lý thành công."
    data: T | None = None
    meta: M | None = None

class StandardResponse(BaseModel, Generic[T, M]):
    detail: DetailResponse[T, M]
