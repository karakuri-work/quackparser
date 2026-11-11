# QuackParser

## exec

```shell
uv run fastapi dev app/main.py
```

## test

```shell
uv run python -m pytest
```

## API

### `POST /convert`

Docling でドキュメントを Markdown に変換します。`multipart/form-data` ではなく
**JSON** を受け取り、**JSON** で返します。

**リクエストボディ**

```json
{
  "content": "base64_encoded_bytes",
  "name": "document_name"
}
```

- `content`: 変換対象のバイナリデータを base64 文字列で渡します。
- `name`: ドキュメント名（例: `report.pdf`）。変換結果に反映されます。

**レスポンス**

```json
{
  "success": true,
  "name": "report.pdf",
  "markdown": "# Title\n\n...",
  "error": null
}
```

失敗時は `success: false`、`error` に原因が記載されます（例: base64 が不正な場合）。

### `GET /`

フロントエンド（HTML）を返します。
