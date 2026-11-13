from __future__ import annotations

from pathlib import Path

from docling.document_converter import DocumentConverter
from fastapi import Depends, FastAPI, File, Response, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.schemas import ConvertErrorResponse, ConvertSuccessResponse, HealthResponse
from app.services import DocumentService

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="QuackParser API",
    version="0.1.0",
    summary="Document to Markdown Conversion Service",
    description=(
        "A document conversion API powered by Docling."
        "It converts various file formats, including PDF, Microsoft Office documents"
        " (DOCX, PPTX, XLSX), and images (PNG, JPG), into structured Markdown."
    ),
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

doc_converter = DocumentConverter()
document_service = DocumentService(doc_converter)


def get_document_service() -> DocumentService:

    return document_service


@app.post(
    "/api/v1/convert",
    summary="Convert Document to Markdown",
    description="Converts a document into structured Markdown.",
    responses={
        200: {
            "model": ConvertSuccessResponse,
            "description": "Successful conversion.",
        },
        500: {
            "model": ConvertErrorResponse,
            "description": "Conversion Error.",
        },
    },
)
async def convert(
    response: Response,
    file: UploadFile = File(
        description=(
            "The file to be converted into Markdown (e.g., PDF,"
            " DOCX, PPTX, XLSX, PNG, JPG, etc.)."
        )
    ),
    service: DocumentService = Depends(get_document_service),
) -> ConvertSuccessResponse | ConvertErrorResponse:
    try:
        content = await file.read()
    except Exception as exc:
        response.status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
        return ConvertErrorResponse(error=str(exc))
    try:
        markdown = service.convert_content(content)
        response.status_code = status.HTTP_200_OK
        return ConvertSuccessResponse(markdown=markdown)
    except Exception as exc:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return ConvertErrorResponse(error=str(exc))


@app.get(
    "/health",
    summary="Health Check",
    description="Checks the operational status of the service.",
    response_model=HealthResponse,
    responses={
        200: {
            "model": HealthResponse,
            "description": "Successful Health Check.",
        },
    },
)
def health_check(response: Response) -> HealthResponse:
    response.status_code = status.HTTP_200_OK
    return HealthResponse(status="ok")


app.mount("/", StaticFiles(directory=STATIC_DIR, html=True))
