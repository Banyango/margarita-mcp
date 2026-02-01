# Use official Python 3.12 slim image
FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable unbuffered stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system build deps for packages that need compilation
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       gcc \
       libssl-dev \
       libffi-dev \
       curl \
    && rm -rf /var/lib/apt/lists/*

# Copy only lock files first to leverage Docker layer caching
COPY pyproject.toml uv.lock /app/

# Upgrade pip, install the `uv` tool and use it to install locked dependencies
RUN cd /app  \
    && python -m pip install --upgrade pip \
    && pip install --no-cache-dir uv \
    && uv sync

# Copy the rest of the project
COPY . /app

# Ensure src is on PYTHONPATH so `python -m src.main` works
ENV PYTHONPATH="/app/src:${PYTHONPATH}"

# Expose default FastAPI port
EXPOSE 8000

# Default command: run the project's main module which starts uvicorn
CMD ["uv", "run", "python", "src/main.py"]

