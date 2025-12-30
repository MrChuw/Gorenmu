FROM python:3.13-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates build-essential && \
    rm -rf /var/lib/apt/lists/*


# Uv stuff
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


WORKDIR /app

RUN mkdir -p /uv-cache /uv-python

ENV UV_CACHE_DIR=/uv-cache
ENV UV_PYTHON_INSTALL_DIR=/uv-python
ENV UV_PROJECT_ENVIRONMENT=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"
