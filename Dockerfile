# syntax=docker/dockerfile:1

# ---------- Build stage: install dependencies into a venv ----------
FROM python:3.12-slim AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# git is required because requirements.txt installs discord.py from GitHub;
# build-essential covers any packages (e.g. python-Levenshtein) that need compiling.
RUN apt-get update \
    && apt-get install -y --no-install-recommends git build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt


# ---------- Runtime stage ----------
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MPLBACKEND=Agg \
    PATH="/opt/venv/bin:$PATH"

# Run as a non-root user
RUN useradd --create-home --shell /usr/sbin/nologin ermce

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app
COPY --chown=ermce:ermce . .

USER ermce

# Internal FastAPI server (utils/api.py), used by the ERM CE website/panel.
# Listens on BIND_PORT, which defaults to 5000.
EXPOSE 5000
CMD ["python", "main.py"]