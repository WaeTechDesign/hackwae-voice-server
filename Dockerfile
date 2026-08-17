FROM python:3.12-slim-bookworm

# Pin uv to the development environment version.
COPY --from=ghcr.io/astral-sh/uv:0.12.0 /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_NO_DEV=1 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Runtime/system dependencies required by the application and audio stack.
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    ffmpeg \
    git \
    libsndfile1 \
    libgomp1 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency metadata first so Docker can cache dependency installation.
COPY pyproject.toml uv.lock ./

# Install locked dependencies without installing the project itself yet.
RUN uv sync --frozen --no-dev --no-install-project

# Copy application source.
COPY . .

# Install the project using the locked dependency set.
RUN uv sync --frozen --no-dev

# Runtime directories.
RUN mkdir -p \
    /ai/models \
    /ai/voices \
    /app/storage \
    /app/uploads \
    /app/output

EXPOSE 8082

CMD ["/app/.venv/bin/python", "main.py"]
