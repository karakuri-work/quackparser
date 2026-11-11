# QuackParser

QuackParser is a FastAPI-based API service that leverages the advanced **Docling** library to convert uploaded documents into high-quality **Markdown** format.

## 🌟 Features

- **Docling Integration**: Uses state-of-the-art document parsing technology to accurately convert complex layouts into clean, structured Markdown.
- **FastAPI Powered**: Built on a high-performance Python framework, providing a type-safe, fast, and easy-to-use API.
- **In-Memory Processing**: Processes binary data entirely in memory without relying on the filesystem, making it ideal for containerized (Docker) or serverless environments.
- **Clean Architecture**: Follows a modular design with a dedicated service layer, allowing for easy extension and customization of conversion logic.

## 🛠 Tech Stack

- **Language**: Python 3.9+
- **Web Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Document Parsing**: [Docling](https://github.com/DS4SD/docling)
- **Data Validation**: [Pydantic](https://docs.pydantic.dev/)
- **Server**: [Uvicorn](https://www.uvicorn.org/)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/quackparser.git
cd quackparser
```

### 2. Install Dependencies

```bash
uv sync
```

### 3. Run the Server

**For development (with auto-reload):**

```bash
uv run fastapi dev app/main.py
```

**For production:**

```bash
uv run fastapi run app/main.py
```

Once started, you can access the default frontend at `http://127.0.0.1:8000`.
You can also explore the interactive API documentation (Swagger UI) at `http://127.0.0.1:8000/docs`.

## 🧪 Testing

To run the tests, use the following command:

```bash
uv run python -m pytest
```

## 🔌 API Specification

### Document Conversion

Convert an uploaded file to Markdown format.

- **Endpoint**: `POST /convert`
- **Content-Type**: `multipart/form-data`
- **Request Body**:
  - `file`: The file to be converted (PDF, DOCX, etc.)
- **Response**:
  - `success` (bool): Indicates if the conversion was successful.
  - `markdown` (str | null): The resulting Markdown text.
  - `error` (str | null): Error message (returned if `success` is false).

**Example using `curl`:**

```bash
curl -X POST "http://127.0.0.1:8000/convert" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@example.pdf"
```

## 📂 Project Structure

```text
app/
├── __init__.py
├── main.py          # FastAPI application entry point
├── schemas.py       # Pydantic data models
├── services.py      # Docling-based conversion logic
└── static/          # Frontend assets (index.html, etc.)
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.
