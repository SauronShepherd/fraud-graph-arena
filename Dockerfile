# syntax=docker/dockerfile:1.7
FROM node:22-bookworm-slim AS web-build
ENV NPM_CONFIG_UPDATE_NOTIFIER=false
WORKDIR /workspace/apps/web
COPY apps/web/package.json apps/web/package-lock.json ./
RUN npm ci --no-audit --no-fund --no-update-notifier --loglevel=error
COPY apps/web/ ./
RUN npm run build

FROM python:3.13-slim AS runtime
ARG FGA_SOURCE_REVISION=working-tree
LABEL org.opencontainers.image.revision=$FGA_SOURCE_REVISION
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    FGA_PROJECT_ROOT=/app \
    FGA_ENVIRONMENT=production \
    FGA_RUNTIME_ROLE=WEB \
    FGA_ROUND_REPOSITORY=sqlite \
    FGA_SQLITE_PATH=/data/fga.sqlite3 \
    FGA_FRONTEND_DIST=/app/apps/web/dist \
    FGA_ALLOWED_ORIGINS=[]
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src/ ./src/
COPY contracts/ ./contracts/
COPY config/ ./config/
COPY case-data/ ./case-data/
COPY case-packages/ ./case-packages/
RUN python -m pip install --disable-pip-version-check --no-cache-dir --root-user-action=ignore .
COPY --from=web-build /workspace/apps/web/dist ./apps/web/dist
RUN mkdir -p /data
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=3s --retries=5 CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/v1/health/ready', timeout=2)"]
CMD ["python", "-m", "fraud_graph_arena.runtime"]
