# Build frontend assets
FROM node:26-trixie-slim AS node-builder
WORKDIR /opt/quackparser

COPY Frontend/package*.json ./
RUN npm install

COPY Frontend ./
RUN npm run build

# Build python environment
FROM python:3.14-slim-trixie AS python-builder
WORKDIR /opt/quackparser

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY Backend/pyproject.toml Backend/uv.lock ./
RUN uv sync --frozen --no-dev

# Final production image
FROM python:3.14-slim-trixie
WORKDIR /opt/quackparser

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update \
    && apt-get install -y \
        libgl1 \
        libglib2.0-0 \
        curl \
        wget \
        git \
        procps \
    && rm -rf /var/lib/apt/lists/*

ENV ENV HF_HOME=/root/.cache/huggingface \
    TORCH_HOME=/root/.cache/torch \
    DOCLING_ARTIFACTS_PATH=/root/.cache/docling/models \
    OMP_NUM_THREADS=4

COPY Backend ./
COPY --from=node-builder /opt/quackparser/dist ./app/static
COPY --from=python-builder /opt/quackparser/.venv ./.venv

RUN uv run docling-tools models download

CMD ["uv", "run", "fastapi", "run", "app/main.py"]
