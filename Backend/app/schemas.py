from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ConvertResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "success": True,
                    "markdown": "# Markdown",
                    "error": None,
                }
            ]
        }
    )

    success: bool = Field(
        ...,
        description=(
            "Conversion success flag. When `false`, the failure reason "
            "is included in `error`."
        ),
    )
    markdown: str | None = Field(
        default=None,
        description=(
            "The converted Markdown content. Returns the text on success,"
            " otherwise null."
        ),
    )
    error: str | None = Field(
        default=None,
        description="Error message. Contains the message when `success` is `false`.",
    )
