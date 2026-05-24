from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator

VALID_CATEGORIES = {"bug_report", "missing_data", "feature_request", "general"}
VALID_STATUSES = {"new", "in_progress", "fixed", "wont_fix", "duplicate"}


class FeedbackCreate(BaseModel):
    category: str
    name:         str | None = None
    email:        str | None = None
    subject:      str | None = None
    message:      str
    page_context: str | None = None

    model_config = ConfigDict(str_strip_whitespace=True)

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str) -> str:
        if v not in VALID_CATEGORIES:
            raise ValueError(f"category must be one of {sorted(VALID_CATEGORIES)}")
        return v

    @field_validator("message")
    @classmethod
    def validate_message(cls, v: str) -> str:
        if not v or len(v.strip()) < 10:
            raise ValueError("message must be at least 10 characters")
        if len(v) > 5000:
            raise ValueError("message must be 5000 characters or fewer")
        return v


class FeedbackStatusUpdate(BaseModel):
    status: str
    resolution_note: str | None = None

    model_config = ConfigDict(str_strip_whitespace=True)

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        if v not in VALID_STATUSES:
            raise ValueError(f"status must be one of {sorted(VALID_STATUSES)}")
        return v


class FeedbackResponse(BaseModel):
    id:              UUID
    category:        str
    name:            str | None
    email:           str | None
    subject:         str | None
    message:         str
    page_context:    str | None
    status:          str
    resolved_at:     datetime | None
    resolution_note: str | None
    created_at:      datetime

    model_config = ConfigDict(from_attributes=True)
