from __future__ import annotations

from io import BytesIO

from docling.document_converter import DocumentConverter
from docling_core.types.io import DocumentStream


class DocumentService:
    def __init__(self, converter: DocumentConverter) -> None:
        self.converter = converter

    def convert_content(self, content: bytes) -> str:
        result = self.converter.convert(
            DocumentStream(name="document", stream=BytesIO(content))
        )
        return result.document.export_to_markdown()
