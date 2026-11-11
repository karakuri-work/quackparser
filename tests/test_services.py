"""Unit tests for the document conversion service."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from app.services import DocumentService, DocumentStream


def make_service(converter=None) -> DocumentService:
    """Build a service, optionally with a mocked converter."""
    if converter is None:
        converter = MagicMock()
    return DocumentService(converter)


def test_convert_content_passes_bytes() -> None:
    """The converter is given a DocumentStream wrapping the raw bytes."""
    payload = b"<html><body>Hi</body></html>"
    converter = MagicMock()
    fake_result = MagicMock()
    fake_result.document.export_to_markdown.return_value = "# Hi"
    converter.convert.return_value = fake_result

    service = make_service(converter)
    markdown = service.convert_content(payload)

    assert markdown == "# Hi"
    source = converter.convert.call_args.args[0]
    assert isinstance(source, DocumentStream)
    assert source.name == "document"
    assert source.stream.getvalue() == payload


def test_convert_content_propagates_errors() -> None:
    """A converter failure surfaces as an exception to the caller."""
    converter = MagicMock()
    converter.convert.side_effect = RuntimeError("boom")
    service = make_service(converter)
    with pytest.raises(RuntimeError, match="boom"):
        service.convert_content(b"data")
