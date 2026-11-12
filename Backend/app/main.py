"""QuackParser API — FastAPI application."""

from __future__ import annotations

from pathlib import Path

from fastapi import Depends, FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse

from app.schemas import ConvertResponse
from app.services import DocumentService

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="QuackParser API",
    version="0.1.0",
    summary="Docling-based document conversion service",
    description=(
        "Document conversion API using Docling."
        "Converts PDF, Office documents, images, etc., to Markdown."
    ),
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/",
    response_class=HTMLResponse,
    summary="Web UI",
    description="Returns a Web UI (HTML) for the browser.",
)
async def read_index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


def get_document_service() -> DocumentService:
    """Provide a document service wired to Docling."""
    from docling.document_converter import DocumentConverter

    return DocumentService(DocumentConverter())


@app.post(
    "/convert",
    response_model=ConvertResponse,
    summary="Convert document to Markdown",
    description=(
        "Converts uploaded documents to Markdown using Docling."
        "Upload the file as multipart/form-data in the 'file' field."
        "Returns 200 with `success: false` and an error message if conversion fails."
    ),
    responses={
        200: {
            "model": ConvertResponse,
            "description": (
                "Returns `success: true` and the Markdown content on success;"
                " otherwise, returns `success: false` with an error message."
            ),
            "content": {
                "example": {
                    "success": True,
                    "markdown": "# Title\n\nConverted text...",
                    "error": None,
                },
                "example2": {
                    "success": False,
                    "markdown": None,
                    "error": "Conversion failed: ...",
                },
            },
        },
        422: {
            "description": "The file upload is missing or invalid.",
            "content": {
                "example": {
                    "detail": [
                        {
                            "loc": ["body", "file"],
                            "msg": "Field required",
                            "type": "value_error.missing",
                        }
                    ]
                }
            },
        },
    },
)
async def convert(
    file: UploadFile = File(
        ...,
        description="The file to convert (PDF, DOCX, PPTX, XLSX, PNG, JPG, etc.).",
    ),
    service: DocumentService = Depends(get_document_service),
) -> ConvertResponse:
    """Convert uploaded document bytes to Markdown."""
    try:
        content = await file.read()
    except Exception as exc:
        return ConvertResponse(success=False, error=str(exc))

    try:
        markdown = service.convert_content(content)
        return ConvertResponse(success=True, markdown=markdown)
    except Exception as exc:
        return ConvertResponse(success=False, error=str(exc))
