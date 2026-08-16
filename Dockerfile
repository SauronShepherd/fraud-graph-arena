# syntax=docker/dockerfile:1.7
FROM node:22-bookworm-slim AS web-build
WORKDIR /workspace/apps/web
COPY apps/web/package.json apps/web/package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY apps/web/ ./
RUN npm run build

FROM python:3.13-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FGA_ENVIRONMENT=production \
    FGA_RUNTIME_ROLE=WEB \
    FGA_ROUND_REPOSITORY=sqlite \
    FGA_SQLITE_PATH=/data/fga.sqlite3 \
    FGA_FRONTEND_DIST=/app/apps/web/dist \
    FGA_ALLOWED_ORIGINS=[]
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src/ ./src/
RUN python -m pip install --no-cache-dir .
COPY --from=web-build /workspace/apps/web/dist ./apps/web/dist
RUN mkdir -p /data
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "fraud_graph_arena.web.main:app", "--host", "0.0.0.0", "--port", "8000"]
