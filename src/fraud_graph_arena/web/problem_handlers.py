from __future__ import annotations

from typing import Any
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from fraud_graph_arena.shared.errors import FgaError

PROBLEM_MEDIA_TYPE = "application/problem+json"


def correlation_id(request: Request) -> str:
    return getattr(request.state, "correlation_id", str(uuid4()))


def problem_response(
    request: Request,
    *,
    status: int,
    code: str,
    title: str,
    detail: str,
    recovery: str | None = None,
    errors: list[dict[str, Any]] | None = None,
) -> JSONResponse:
    payload: dict[str, Any] = {
        "type": f"https://fraud-graph-arena.invalid/problems/{code.lower().replace('_', '-')}",
        "title": title,
        "status": status,
        "detail": detail,
        "instance": request.url.path,
        "code": code,
        "correlation_id": correlation_id(request),
    }
    if recovery is not None:
        payload["recovery"] = recovery
    if errors is not None:
        payload["errors"] = errors
    return JSONResponse(payload, status_code=status, media_type=PROBLEM_MEDIA_TYPE)


def register_problem_handlers(app: FastAPI) -> None:
    @app.exception_handler(FgaError)
    async def handle_fga_error(request: Request, exc: FgaError) -> JSONResponse:
        return problem_response(
            request,
            status=exc.status,
            code=exc.code,
            title=exc.title,
            detail=exc.detail,
            recovery=exc.recovery,
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        safe_errors = [
            {
                "location": [str(part) for part in item["loc"]],
                "message": item["msg"],
                "type": item["type"],
            }
            for item in exc.errors()
        ]
        return problem_response(
            request,
            status=422,
            code="REQUEST_VALIDATION_FAILED",
            title="Request validation failed",
            detail="The request did not match the public API contract.",
            recovery="Correct the identified fields and submit the request again.",
            errors=safe_errors,
        )
    @app.exception_handler(StarletteHTTPException)
    async def handle_http_error(
        request: Request,
        exc: StarletteHTTPException,
    ) -> JSONResponse:
        code_by_status = {
            404: "ROUTE_NOT_FOUND",
            405: "METHOD_NOT_ALLOWED",
        }
        code = code_by_status.get(exc.status_code, "HTTP_ERROR")
        title = {
            404: "Route not found",
            405: "Method not allowed",
        }.get(exc.status_code, "Request failed")
        return problem_response(
            request,
            status=exc.status_code,
            code=code,
            title=title,
            detail=str(exc.detail),
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
        # Detailed diagnostics belong in server logs. The public contract remains safe.
        return problem_response(
            request,
            status=500,
            code="INTERNAL_ERROR",
            title="The investigation hit an unexpected wall",
            detail="The request could not be completed.",
            recovery="Retry the operation. Use the correlation reference if the problem persists.",
        )
