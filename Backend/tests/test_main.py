from __future__ import annotations

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app

HTML = b"<html><body>Hello</body></html>"


@pytest.fixture
def client_and_mock() -> Generator[tuple[TestClient, MagicMock], None, None]:
    mocked = MagicMock()
    mocked.convert_content.return_value = "# Hello"
    with patch("app.main.document_service", mocked):
        yield TestClient(app), mocked


def test_convert_success(client_and_mock: tuple[TestClient, MagicMock]) -> None:
    client, _ = client_and_mock
    resp = client.post(
        "/api/v1/convert",
        files={"file": ("test.html", HTML)},
    )

    assert resp.status_code == 200
    body = resp.json()
    assert body["markdown"] == "# Hello"


def test_convert_missing_fields(client_and_mock: tuple[TestClient, MagicMock]) -> None:
    client, _ = client_and_mock
    resp = client.post("/api/v1/convert", files={})
    assert resp.status_code == 422


def test_health_check(client_and_mock: tuple[TestClient, MagicMock]) -> None:
    client, _ = client_and_mock
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_convert_error_503(client_and_mock: tuple[TestClient, MagicMock]) -> None:
    client, mocked = client_and_mock
    # 変換時に例外を発生させるように設定
    mocked.convert_content.side_effect = Exception("Conversion failed")

    resp = client.post(
        "/api/v1/convert",
        files={"file": ("test.pdf", b"dummy content")},
    )

    assert resp.status_code == 503
    body = resp.json()
    assert "error" in body
    assert body["error"] == "Conversion failed"
