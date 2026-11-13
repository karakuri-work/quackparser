from __future__ import annotations

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(
        examples=["ok"],
    )


class ConvertSuccessResponse(BaseModel):
    markdown: str = Field(
        examples=["# Markdown\n\n## Conversion"],
    )


class ConvertErrorResponse(BaseModel):
    error: str = Field(
        examples=["Error Message."],
    )
