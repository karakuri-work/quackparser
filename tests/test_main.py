"""Integration tests for the /convert endpoint."""

from __future__ import annotations

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app

HTML = b"<html><body>Hello</body></html>"


@pytest.fixture
def client_and_mock() -> Generator[tuple[TestClient, MagicMock], None, None]:
    """Client with the DocumentService dependency swapped for a mock.

    The patch stays active for the whole test body via ``yield``.
    """
    mocked = MagicMock()
    mocked.convert_content.return_value = "# ok"
    with patch("app.main.DocumentService", return_value=mocked):
        yield TestClient(app), mocked


def test_convert_success(client_and_mock: tuple[TestClient, MagicMock]) -> None:
    """Successful conversion returns Markdown content from a multipart file."""
    client, _ = client_and_mock
    resp = client.post(
        "/convert",
        files={"file": ("test.html", HTML)},
    )

    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert body["markdown"] == "# ok"


def test_convert_missing_fields(client_and_mock: tuple[TestClient, MagicMock]) -> None:
    """Missing required fields result in a validation error (422)."""
    client, _ = client_and_mock
    resp = client.post("/convert", files={})
    assert resp.status_code == 422
