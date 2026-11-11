"""Pydantic models for request/response validation."""

from __future__ import annotations

from pydantic import BaseModel


class ConvertResponse(BaseModel):
    """Result of a conversion request."""

    success: bool
    markdown: str | None = None
    error: str | None = None
