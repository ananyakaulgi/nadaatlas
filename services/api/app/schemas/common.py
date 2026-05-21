from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class PaginationParams(BaseModel):
    skip: int = 0
    limit: int = 20

    model_config = ConfigDict(from_attributes=True)


class PaginatedResponse(BaseModel, Generic[T]):  # noqa: UP046
    items: list[T]
    total: int
    skip: int
    limit: int

    model_config = ConfigDict(from_attributes=True)


class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str

    model_config = ConfigDict(from_attributes=True)


class ErrorDetail(BaseModel):
    field: str
    message: str

    model_config = ConfigDict(from_attributes=True)


class ErrorResponse(BaseModel):
    error: str
    details: list[ErrorDetail] | None = None

    model_config = ConfigDict(from_attributes=True)
