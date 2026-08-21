from pathlib import Path

ROOT = Path(__file__).parents[2]

def test_backend_has_no_frontend_screen_interpreter_or_screen_endpoint():
    source = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "src/fraud_graph_arena").rglob("*.py"))
    assert "class Screen" not in source
    assert '"/screens"' not in source
    assert "screen_set.schema" not in source
