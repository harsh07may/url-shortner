from pydantic import BaseModel, Field, HttpUrl, field_validator

RESERVED = {"docs", "redoc", "openapi.json", "links", "health"}

class LinkCreate(BaseModel):
    """Request body for creating a short link."""
    url: HttpUrl              
    code: str | None = Field(default=None,
                             min_length=6, max_length=16,
                             pattern=r"^[A-Za-z0-9_-]+$")
    @field_validator("code")
    @classmethod
    def not_reserved(cls, v: str | None) -> str | None:
        if v in RESERVED:
            raise ValueError("this code is reserved")
        return v

class LinkOut(BaseModel):
    code: str
    short_url: str
    target_url: str
    clicks: int = 0