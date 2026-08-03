from pathlib import Path

from fastapi.testclient import TestClient

from fraud_graph_arena.application import create_app
from fraud_graph_arena.config import Settings


def test_production_frontend_refresh_falls_back_to_index_html(tmp_path: Path) -> None:
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "index.html").write_text("<main>FGA shell</main>", encoding="utf-8")
    settings = Settings(
        environment="test",
        round_repository="memory",
        frontend_dist=dist,
        allowed_origins=["http://testserver"],
    )

    with TestClient(create_app(settings)) as client:
        board = client.get("/rounds/round-1/board")
        intro = client.get("/rounds/round-1/intro?page=2")

    assert board.status_code == 200
    assert intro.status_code == 200
    assert board.text == "<main>FGA shell</main>"
    assert intro.text == "<main>FGA shell</main>"
    assert board.headers["content-type"].startswith("text/html")


def test_missing_static_asset_remains_a_real_404(tmp_path: Path) -> None:
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "index.html").write_text("<main>FGA shell</main>", encoding="utf-8")
    settings = Settings(
        environment="test",
        round_repository="memory",
        frontend_dist=dist,
        allowed_origins=["http://testserver"],
    )

    with TestClient(create_app(settings), raise_server_exceptions=False) as client:
        response = client.get("/assets/missing.js")

    assert response.status_code == 404
    assert "FGA shell" not in response.text
