FROM python:3.12-slim AS base

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Install dependencies (cached layer)
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev --no-install-project

# Copy source and install project
COPY src/ src/
RUN uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src:$PYTHONPATH"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
