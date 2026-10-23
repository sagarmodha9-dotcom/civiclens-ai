# CivicLens API image: FastAPI + the pinned, versioned DuckDB snapshot baked in at build time.
# Build:  docker build --build-arg SNAPSHOT_URL=https://github.com/<owner>/civiclens-ai/releases/download/snapshot-<v>/civiclens_<v>.duckdb \
#                      --build-arg SNAPSHOT_SHA256=<sha> -t civiclens-api api/
FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
RUN adduser --disabled-password --gecos "" app
COPY api/pyproject.toml api/
COPY api/civiclens_api api/civiclens_api
RUN pip install -q ./api
ARG SNAPSHOT_URL
ARG SNAPSHOT_SHA256
RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends curl ca-certificates >/dev/null && rm -rf /var/lib/apt/lists/* \
 && mkdir -p /data && curl -fsSL "$SNAPSHOT_URL" -o /data/civiclens.duckdb \
 && echo "$SNAPSHOT_SHA256  /data/civiclens.duckdb" | sha256sum -c - \
 && chown -R app:app /data
USER app
ENV CIVICLENS_SNAPSHOT=/data/civiclens.duckdb CIVICLENS_LEDGER=/data/ledger/investigator_ledger.json CIVICLENS_ANSWER_CACHE=/data/ledger/investigator_cache.json
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s CMD curl -fsS http://localhost:8000/healthz || exit 1
CMD ["uvicorn", "civiclens_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
