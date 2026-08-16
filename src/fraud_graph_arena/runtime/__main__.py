from fraud_graph_arena.config import RuntimeRole, Settings


def main() -> int:
    settings = Settings()
    if settings.runtime_role == RuntimeRole.WEB:
        import uvicorn

        uvicorn.run("fraud_graph_arena.runtime.web:app", host="0.0.0.0", port=8000)
        return 0
    if settings.runtime_role == RuntimeRole.MAINTENANCE:
        from .maintenance import run
    elif settings.runtime_role == RuntimeRole.EVALUATOR:
        from .evaluator import run
    else:
        from .migrate import run
    return run(settings)


raise SystemExit(main())
