"""QuackParser API — FastAPI application."""

from __future__ import annotations

from pathlib import Path

from fastapi import Depends, FastAPI, File, UploadFile
from fastapi.responses import FileResponse, HTMLResponse

from app.schemas import ConvertResponse
from app.services import DocumentService

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="QuackParser API")


@app.get("/", response_class=HTMLResponse)
async def read_index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


def get_document_service() -> DocumentService:
    """Provide a document service wired to Docling."""
    from docling.document_converter import DocumentConverter

    return DocumentService(DocumentConverter())


@app.post("/convert", response_model=ConvertResponse)
async def convert(
    file: UploadFile = File(...),
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
