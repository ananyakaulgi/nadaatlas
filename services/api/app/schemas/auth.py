from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class LoginRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    password: str = Field(min_length=1)
    totp_code: str | None = Field(
        default=None,
        description="6-digit TOTP code — required when TOTP is enabled on the account",
    )


class TokenResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(description="Access token lifetime in seconds")


class RefreshRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    refresh_token: str


class TOTPSetupResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    secret: str = Field(description="Base32 TOTP secret — display once, then discard")
    qr_uri: str = Field(description="otpauth:// URI for QR code generation")
    backup_codes: list[str] = Field(
        description="One-time backup codes — show to user exactly once"
    )


class TOTPVerifyRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    totp_code: str = Field(min_length=6, max_length=6, pattern=r"^\d{6}$")


class ChangePasswordRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    current_password: str = Field(min_length=1)
    new_password: str = Field(
        min_length=12,
        description="Minimum 12 characters",
    )

    @field_validator("new_password")
    @classmethod
    def new_password_strength(cls, v: str) -> str:
        errors: list[str] = []
        if not any(c.isupper() for c in v):
            errors.append("at least one uppercase letter")
        if not any(c.islower() for c in v):
            errors.append("at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            errors.append("at least one digit")
        if not any(c in r"""!@#$%^&*()_+-=[]{}|;':",.<>?/`~""" for c in v):
            errors.append("at least one special character")
        if errors:
            raise ValueError(f"Password must contain: {', '.join(errors)}")
        return v


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    is_active: bool
    totp_enabled: bool
    last_login: datetime | None = None
