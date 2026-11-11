"""Document conversion business logic."""

from __future__ import annotations

from io import BytesIO

from docling.document_converter import DocumentConverter
from docling_core.types.io import DocumentStream


class DocumentService:
    """Encapsulates document conversion using Docling.

    Accepts raw document bytes and returns the parsed Markdown
    without interacting with the filesystem.
    """

    def __init__(self, converter: DocumentConverter) -> None:
        self.converter = converter

    def convert_content(self, content: bytes) -> str:
        """Convert raw document bytes to Markdown.

        Args:
            content: The raw bytes of the document.

        Returns:
            The parsed Markdown text.

        Raises:
            Exception: If the conversion fails.
        """
        result = self.converter.convert(
            DocumentStream(name="document", stream=BytesIO(content))
        )
        return result.document.export_to_markdown()
